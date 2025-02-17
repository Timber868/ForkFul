<template>
    <nav class="navbar">
      <RouterLink class="nav-link" to="/">Home</RouterLink>
      <RouterLink class="nav-link" to="/login">Login</RouterLink>
      <RouterLink class="nav-link" to="/register">Register</RouterLink>
      <RouterLink class="nav-link" to="/feed">Feed</RouterLink>
      <RouterLink class="nav-link" to="/profile">Profile</RouterLink>
      <RouterLink class="nav-link" to="/post">Post</RouterLink>
        <img :src="forfulLogo" alt="Forkful Logo" style="width: 70px; height: 70px;" />
    </nav>
  </template>
  
  <script setup lang="ts">
    import forfulLogo from '../assets/forkfullogo.png';
  </script>
  
  <style scoped>
  .navbar {
    position: fixed;    
    top: 0;
    left: 0;
    width: 100%;       
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 1rem 2rem;
    background: linear-gradient(90deg, #161d23, #0f444c);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    z-index: 1000;         
  }
  
  .nav-link {
    color: #d2e1cc;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: all 0.3s ease;
    position: relative;
  }
  
  .nav-link:hover {
    background-color: #114538;
    color: #d2e1cc;
    transform: translateY(-2px);
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
    color: #d2e1cc;
  }
  </style>
  