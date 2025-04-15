import { createI18n } from 'vue-i18n';

const messages = {
    en: {
        message: {
            hello: 'hello world',
            dashboard: 'Dashboard',
            login: 'Login',
            routes: 'Routes',
            add_route: 'Add Route',
            logout: 'Logout'
        }
    },
    zh: {
        message: {
            hello: '你好，世界',
            dashboard: '仪表盘',
            login: '登录',
            routes: '路由列表',
            add_route: '添加路由',
            logout: '登出'
        }
    }
};

const i18n = createI18n({
    locale: 'en',
    messages
});

export default i18n;



