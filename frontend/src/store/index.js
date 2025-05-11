import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        is_login: localStorage.getItem('is_login') || false
    }),
    actions: {
        setLogin(login_state) {
            this.is_login = login_state;
            localStorage.setItem('is_login', login_state);
        },
        setToken(token) {
            this.token = token;
            localStorage.setItem('token', token);
        },
        clearToken() {
            this.token = null;
            localStorage.removeItem('token');
        }
    },
});