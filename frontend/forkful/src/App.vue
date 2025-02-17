<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div>
    <Navbar/>
    <div class="content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.content {
  padding-top: 70px; 
}
</style>
