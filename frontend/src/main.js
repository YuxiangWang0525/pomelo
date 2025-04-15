import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index.js';
import { createPinia } from 'pinia';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import i18n from './i18n/index';

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.use(Antd);
app.use(i18n);

app.mount('#app');



