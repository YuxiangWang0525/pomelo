<template>
  <a-config-provider :locale="currentLocale">
    <a-layout style="min-height: 100vh">
      <a-layout-header class="header">
<!--        <h1 class="logo">Pomelo</h1>-->
        <a-menu theme="dark" mode="horizontal" :default-selected-keys="['2']">
          <a-menu-item key="1" v-if="isAuthenticated">
            {{ $t('message.dashboard') }}
          </a-menu-item>
          <a-menu-item key="2" v-if="isAuthenticated">
            <router-link to="/routes">{{ $t('message.routes') }}</router-link>
          </a-menu-item>
          <a-menu-item key="3" v-if="isAuthenticated">
            <router-link to="/add-route">{{ $t('message.add_route') }}</router-link>
          </a-menu-item>
          <a-menu-item key="4" @click="logout" v-if="isAuthenticated">
            {{ $t('message.logout') }}
          </a-menu-item>
          <a-menu-item key="5" v-if="!isAuthenticated">
            {{ $t('message.login') }}
          </a-menu-item>
          <a-menu-item key="6" @click="toggleLocale">
            {{ locale.value === 'zh' ? 'English' : '中文' }}
          </a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 0 50px">
        <a-breadcrumb style="margin: 16px 0">
          <a-breadcrumb-item>{{ $route.name }}</a-breadcrumb-item>
        </a-breadcrumb>
        <router-view />
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        Pomelo(NAT Pointer) by YuxiangWang0525 @ 2025
      </a-layout-footer>
    </a-layout>
  </a-config-provider>
</template>

<script setup>
import { ref, computed,watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { ConfigProvider } from 'ant-design-vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/index';
const userstore = useUserStore()
const isAuthenticated = ref(false);
userstore.$subscribe((mutation, is_login) => {
  isAuthenticated.value = is_login;
  console.log("Now State:"+isAuthenticated.value);
})

// 路由、退出登录逻辑
const router = useRouter();
const userStore = useUserStore();

const logout = () => {
  userStore.clearToken();
  router.push('/login');
  userStore.setLogin(false);
  isAuthenticated.value = false;
  location.reload();
};

// 多语言逻辑开始
const { locale } = useI18n();

const toggleLocale = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh';
};

const enUS = ref(null);
const zhCN = ref(null);

// Load Ant Design Vue locales asynchronously
import('ant-design-vue/es/locale/en_US').then(module => {
  enUS.value = module.default;
});
import('ant-design-vue/es/locale/zh_CN').then(module => {
  zhCN.value = module.default;
});

const currentLocale = computed(() => {
  if (locale.value === 'zh' && zhCN.value) {
    return zhCN.value;
  }
  return enUS.value || {};
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body {
  margin: 0;
  padding: 0;
}
.logo {
  width: 120px;
  height: 31px;
  background: rgba(255, 255, 255, 0.2);
  margin-right: 16px;
}
</style>