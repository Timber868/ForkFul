<template>
  <nav class="navbar">
    <img :src="forfulLogo" alt="Forkful Logo" class="logo" />
    <div class="nav-links">
      <RouterLink class="nav-link" to="/">Home</RouterLink>
      <RouterLink class="nav-link" to="/login">Login</RouterLink>
      <RouterLink class="nav-link" to="/register">Register</RouterLink>
      <RouterLink class="nav-link" to="/feed">Feed</RouterLink>
      <RouterLink class="nav-link" to="/profile">Profile</RouterLink>
      <RouterLink class="nav-link" to="/post">Post</RouterLink>

      <button class="nav-link" @click="handleLogout">Logout</button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import axios from 'axios';
import { useRouter } from 'vue-router';
import forfulLogo from '../assets/forkfullogo.png';

const router = useRouter();

function handleLogout() {
  // If your server expects credentials (cookies) for session management,
  // include `{ withCredentials: true }` in the request config.
  axios.post('http://localhost:5001/auth/logout', {}, { withCredentials: true })
    .then(response => {
      console.log(response.data.message); // 'Logged out successfully.'

      // Optionally redirect the user back to login, home, etc.
      router.push('/login');
    })
    .catch(err => {
      console.error('Logout failed:', err);
    });
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  align-items: center;   
  justify-content: flex-start;
  padding: 0.5rem 1rem; 
  background: linear-gradient(90deg, #161d23, #0f444c);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.logo {
  width: 50px;     
  height: 50px;
  margin-right: 30rem;  
}

.nav-links {
  display: flex;
  gap: 1rem;
  font-weight: normal;
}

.nav-link {
  color: #d2e1cc;
  text-decoration: none;
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
  border: none;
  background: none;
  cursor: pointer;
}

.nav-link:hover {
  background-color: #114538;
  transform: translateY(-1px);
}

.nav-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 2px;
  background-color: #5e8d83;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.router-link-active {
  background-color: #114538;
}
</style>