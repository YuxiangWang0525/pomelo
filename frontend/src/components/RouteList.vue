<template>
  <a-table :columns="columns" :data-source="routes" row-key="host">
    <template #action="{ text, record }">
      <a-space size="middle">
        <a-button type="link" @click="deleteRoute(record.host)">
          Delete
        </a-button>
      </a-space>
    </template>
  </a-table>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const columns = [
      {
        title: 'Host',
        dataIndex: 'host',
        key: 'host'
      },
      {
        title: 'Target',
        dataIndex: 'target',
        key: 'target'
      },
      {
        title: 'Type',
        dataIndex: 'type',
        key: 'type'
      },
      {
        title: 'Action',
        key: 'action',
        slots: { customRender: 'action' }
      }
    ];

    const routes = ref([]);

    const fetchRoutes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/admin/routes');
        routes.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    const deleteRoute = async (host) => {
      try {
        await axios.delete(`http://localhost:5000/api/admin/routes/${host}`);
        fetchRoutes();
      } catch (error) {
        console.error(error);
      }
    };

    onMounted(fetchRoutes);

    return {
      columns,
      routes,
      deleteRoute
    };
  }
};
</script>



