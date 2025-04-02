<template>
  <div class="container">
    <div class="form-wrapper">
      <h1 class="title">User Management</h1>
      <div class="grid gap-4 w-full">
        <div v-for="user in users" :key="user.id" class="user-card">
          <div class="user-details">
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Status:</strong> {{ user.status }}</p>
          </div>
          <div>
            <button
              v-if="user.status !== 'banned'"
              @click="handleBan(user.id)"
              :disabled="banning === user.id"
              class="ban-btn"
            >
              {{ banning === user.id ? 'Banning...' : 'Ban User' }}
            </button>
            <span v-else class="banned-text">Banned</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const users = ref([]);
const banning = ref(null);

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/users/');
    users.value = response.data;
  } catch (err) {
    console.error('Failed to fetch users', err);
  }
};

const handleBan = async (userId) => {
  try {
    banning.value = userId;
    await axios.put(`http://127.0.0.1:5000/users/${userId}/ban`);
    const user = users.value.find(u => u.id === userId);
    if (user) user.status = 'banned';
  } catch (err) {
    console.error('Failed to ban user', err);
  } finally {
    banning.value = null;
  }
};

onMounted(fetchUsers);
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background: rgba(210, 225, 204, 0.4);
  min-height: 90vh;
  backdrop-filter: blur(10px);
}

.form-wrapper {
  width: 100%;
  max-width: 600px;
  background: rgba(210, 225, 204, 0.4);
  border-radius: 12px;
  border: 1px solid #114538;
  padding: 2rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #114538;
  margin-bottom: 1.5rem;
  text-align: center;
}

.user-card {
  background-color: white;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.user-details p {
  margin: 0.3rem 0;
  color: #114538;
}

.ban-btn {
  background-color: #5e8d83;
  color: #d2e1cc;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.ban-btn:hover {
  background-color: #114538;
}

.ban-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.banned-text {
  color: #d32f2f;
  font-weight: bold;
}
</style>


  

