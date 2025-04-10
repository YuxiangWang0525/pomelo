from flask import Flask, request, jsonify, redirect, abort
from functools import wraps
import requests
from database_manager import init_db, authenticate, update_user, get_route_by_host, get_proxy_target

app = Flask(__name__)

# Initialize database and create default user if necessary
init_db()


# Authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_data = request.authorization
        if not auth_data or not authenticate(auth_data.username, auth_data.password):
            abort(401)
        return f(*args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def url_process():
    host = request.host
    route = get_route_by_host(host)

    if route:
        _, target, route_type = route
        if route_type == 'redirect':
            return redirect(target, code=302)
        elif route_type == 'proxy':
            return redirect('/proxy/' + target + '/' + request.full_path, code=307)

    return jsonify({'message': host})


@app.route('/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    host = request.host
    target = get_proxy_target(host)

    if not target:
        return jsonify({'error': 'Proxy target not found for this host'}), 404

    try:
        response = requests.request(
            method=request.method,
            url=target + '/' + path,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.raw.headers.items() if
                   name.lower() not in excluded_headers]
        response = app.response_class(
            response.content,
            status=response.status_code,
            headers=headers
        )
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    username = data['username']
    password = data['password']

    if authenticate(username, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/update_credentials', methods=['POST'])
@requires_auth
def update_credentials():
    data = request.get_json()
    if not data or 'new_username' not in data or 'new_password' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    new_username = data['new_username']
    new_password = data['new_password']

    update_user(new_username, new_password)
    return jsonify({'message': 'Credentials updated successfully'}), 200


@app.route('/protected_resource', methods=['GET'])
@requires_auth
def protected_resource():
    return jsonify({'message': 'This is a protected resource'}), 200


if __name__ == '__main__':
    app.run(debug=True)