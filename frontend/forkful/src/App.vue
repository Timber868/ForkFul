<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
        <RouterLink to="/feed">Feed</RouterLink>
        <RouterLink to="/profile">Profile</RouterLink>
        <RouterLink to="/post">Post</RouterLink>
      </nav>
  <RouterView />
</template>

<style scoped>

</style>
