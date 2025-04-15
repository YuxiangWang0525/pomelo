<template>
  <a-config-provider :locale="currentLocale">
    <router-view />
  </a-config-provider>
</template>

<script>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { ConfigProvider } from 'ant-design-vue';

export default {
  components: {
    AConfigProvider: ConfigProvider
  },
  setup() {
    const { locale } = useI18n();
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

    return {
      currentLocale
    };
  }
};
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
</style>
