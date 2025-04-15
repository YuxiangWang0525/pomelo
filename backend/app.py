from flask import Flask, request, jsonify, redirect, abort, send_from_directory
from functools import wraps
import requests
from database_manager import (
    init_db, authenticate, update_user, get_route_by_host, get_proxy_target, update_route,
    get_all_routes, add_route, delete_route, validate_webhook_accesskey
)
from flask_cors import CORS
app = Flask(__name__, static_folder='static/dist')
CORS(app)
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
        _, target, route_type, _ = route
        if route_type == 'redirect':
            return redirect(target, code=302)
        elif route_type == 'proxy':
            return redirect('/proxy' + request.full_path, code=307)

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


@app.route('/webhook/update_route', methods=['GET'])
def webhook_update_route():
    args = request.args
    if not args or 'accesskey' not in args or 'host' not in args or 'target' not in args or 'type' not in args:
        return jsonify({'error': 'Invalid input'}), 400

    accesskey = args['accesskey']
    host = args['host']
    target = args['target']
    route_type = args['type']

    if validate_webhook_accesskey(host, accesskey):
        update_route(host, target, route_type)
        return jsonify({'message': 'Route updated successfully'}), 200
    else:
        return jsonify({'error': 'Access denied or invalid parameters'}), 403


@app.route('/api/admin', methods=['GET'])
@requires_auth
def admin_dashboard():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/admin/routes', methods=['GET'])
@requires_auth
def get_routes():
    routes = get_all_routes()
    return jsonify(routes)


@app.route('/api/admin/routes', methods=['POST'])
@requires_auth
def add_new_route():
    data = request.get_json()
    if not data or 'host' not in data or 'target' not in data or 'type' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    host = data['host']
    target = data['target']
    route_type = data['type']

    if add_route(host, target, route_type):
        return jsonify({'message': 'Route added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add route'}), 500


@app.route('/api/admin/routes/<string:host>', methods=['DELETE'])
@requires_auth
def delete_route(host):
    if delete_route(host):
        return jsonify({'message': 'Route deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete route'}), 500


if __name__ == '__main__':
    app.run(debug=True)