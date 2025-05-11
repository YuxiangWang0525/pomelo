<template>
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
</template>

<script>
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/index';

export default {
  setup() {

  }
};
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
}


</style>



