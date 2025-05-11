<template>
  <a-form layout="vertical" :model="formState" @finish="onFinish">
    <a-form-item label="Username" name="username" :rules="[{ required: true, message: 'Please input your username!' }]">
      <a-input v-model:value="formState.username" />
    </a-form-item>
    <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Please input your password!' }]">
      <a-input-password v-model:value="formState.password" />
    </a-form-item>
    <a-form-item>
      <a-button type="primary" html-type="submit">
        {{ $t('message.login') }}
      </a-button>
    </a-form-item>
  </a-form>
</template>

<script>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/index';
import axios from 'axios';

export default {
  setup() {
    const formState = reactive({
      username: '',
      password: ''
    });

    const router = useRouter();
    const userStore = useUserStore();

    const onFinish = async (values) => {
      try {
        const response = await axios.post('http://localhost:5000/login', values);
        userStore.setToken(response.data.message);
        userStore.setLogin(true);

        router.push('/');
      } catch (error) {
        console.error(error);
      }
    };

    return {
      formState,
      onFinish
    };
  }
};
</script>

<style scoped>
.ant-form {
  max-width: 300px;
  margin: auto;
  padding-top: 50px;
}
</style>



