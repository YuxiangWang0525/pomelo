<template>
  <a-layout style="min-height: 100vh">
    <a-layout-header class="header">
      <div class="logo" />
      <a-menu theme="dark" mode="horizontal" :default-selected-keys="['2']">
        <a-menu-item key="1">
          {{ $t('message.dashboard') }}
        </a-menu-item>
        <a-menu-item key="2">
          <router-link to="/routes">{{ $t('message.routes') }}</router-link>
        </a-menu-item>
        <a-menu-item key="3">
          <router-link to="/add-route">{{ $t('message.add_route') }}</router-link>
        </a-menu-item>
        <a-menu-item key="4" @click="logout">
          {{ $t('message.logout') }}
        </a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>{{ $route.name }}</a-breadcrumb-item>
      </a-breadcrumb>
      <a-layout style="background: #fff; padding: 24px 0; margin-bottom: 24px">
        <a-row :gutter="[16, 16]">
          <a-col :span="12">
            <a-card title="Card Title" style="width: 100%">
              Content
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card title="Card Title" style="width: 100%">
              Content
            </a-card>
          </a-col>
        </a-row>
      </a-layout>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      Ant Design ©2023 Created by Ant UED
    </a-layout-footer>
  </a-layout>
</template>

<script>
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/index';

export default {
  setup() {
    const router = useRouter();
    const userStore = useUserStore();

    const logout = () => {
      userStore.clearToken();
      router.push('/login');
    };

    return {
      logout
    };
  }
};
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
}

.logo {
  width: 120px;
  height: 31px;
  background: rgba(255, 255, 255, 0.2);
  margin-right: 16px;
}
</style>



