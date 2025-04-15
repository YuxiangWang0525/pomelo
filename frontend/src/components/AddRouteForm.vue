<template>
  <a-form layout="vertical" :model="formState" @finish="onFinish">
    <a-form-item label="Host" name="host" :rules="[{ required: true, message: 'Please input the host!' }]">
      <a-input v-model:value="formState.host" />
    </a-form-item>
    <a-form-item label="Target" name="target" :rules="[{ required: true, message: 'Please input the target!' }]">
      <a-input v-model:value="formState.target" />
    </a-form-item>
    <a-form-item label="Type" name="type" :rules="[{ required: true, message: 'Please select the route type!' }]">
      <a-select v-model:value="formState.type">
        <a-select-option value="redirect">Redirect</a-select-option>
        <a-select-option value="proxy">Proxy</a-select-option>
      </a-select>
    </a-form-item>
    <a-form-item>
      <a-button type="primary" html-type="submit">
        Add Route
      </a-button>
    </a-form-item>
  </a-form>
</template>

<script>
import { reactive } from 'vue';
import axios from 'axios';
import { message } from 'ant-design-vue';

export default {
  setup() {
    const formState = reactive({
      host: '',
      target: '',
      type: ''
    });

    const onFinish = async (values) => {
      try {
        await axios.post('http://localhost:5000/api/admin/routes', values);
        message.success('Route added successfully!');
      } catch (error) {
        console.error(error);
        message.error('Failed to add route.');
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
  max-width: 400px;
  margin: auto;
  padding-top: 50px;
}
</style>



