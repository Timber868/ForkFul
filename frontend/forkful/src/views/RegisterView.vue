<template>
    <div class="register-container">
      <div class="register-card">
        <h1>Forkful Register</h1>
        
        <form @submit.prevent="handleRegister">
          <div class="input-group">
            <label for="name">Name</label>
            <input type="text" id="name" placeholder="Enter your name" v-model="name"/>
          </div>
          <div class="input-group">
            <label for="username">Username</label>
            <input type="text" id="username" placeholder="Enter your username" v-model="username"/>
          </div>
          <div class="input-group">
            <label for="phoneNumber">Phone Number</label>
            <input type="text" id="phoneNumber" placeholder="XXXXXXXXXX" v-model="phoneNumber"/>
          </div>
          <div class="input-group">
            <label for="email">Email</label>
            <input type="text" id="email" placeholder="Enter your email" v-model="email"/>
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" placeholder="Enter your password" v-model="password"/>
          </div>
          <button type="submit">Register</button>
          <div class="footer-links">
            <a href="/login"> Already have an account? Login</a>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
    import {ref} from "vue";
    import axios from "axios";
    import { useRouter } from "vue-router";
    import { useAuthStore } from "@/stores/auth";

    const username = ref("");
    const password = ref("")
    const email = ref("")
    const name = ref("")
    const phoneNumber = ref("")
    const errorMessage = ref("")
    const authStore = useAuthStore();

    const router = useRouter();

    const handleRegister = async () => {
    try {
        const response = await axios.post("http://localhost:5000/auth/register", {
            username: username.value,
            password: password.value,
            email: email.value,
            name: name.value,
            phoneNumber: phoneNumber.value,
        }, {withCredentials: true});

        console.log("Register successful!");
        console.log(response.data);

        if (response.status === 200) {
          authStore.setToken(response.data.token, username.value);
            router.replace('/feed');
        }

    } catch (error: any) {
        if (error.response) {
            // Server responded with an error
            errorMessage.value = error.response.data.message || "An error occurred.";
        } else if (error.request) {
            // Request was made but no response received
            errorMessage.value = "No response from server. Please try again.";
        } else {
            // Other errors (e.g., network issues)
            errorMessage.value = error.message;
        }

        console.error("Register Error: ", errorMessage.value);
        alert(`Error registering: ${errorMessage.value}`);
    }
};


  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 90vh;
    padding: 1rem;
    background-image: url("../assets/loginbackground.webp");
    background-size: cover;     
    background-position: center; 
  }
    
  .register-card {
    background: rgba(210, 225, 204, 0.4);
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    width: 100%;
    border: 1px solid #114538;
  }
    
  .register-card h1 {
    color: #114538;
    margin-bottom: 1.5rem;
    text-align: center;
  }
    
  .input-group {
    margin-bottom: 1rem;
  }
    
  .input-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #0f444c;
    font-weight: 600;
  }
    
  .input-group input {
    width: 100%;
    padding: 0.75rem 0;
    border: none;
    border-bottom: 2px solid #0f444c;
    background: transparent;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
  }
    
  .input-group input:focus {
    border-bottom-color: #5e8d83;
    box-shadow: 0 2px 0 0 #5e8d83;
  }
    
  button[type="submit"] {
    width: 100%;
    padding: 0.75rem;
    background-color: #5e8d83;
    color: #d2e1cc;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 15px;
    margin-bottom: 15px;
  }
    
  button[type="submit"]:hover {
    background-color: #114538;
  }
    
  .footer-links {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
  }
    
  .footer-links a {
    color: #0f444c;
    text-decoration: none;
    font-size: 0.9rem;
  }
    
  .footer-links a:hover {
    text-decoration: underline;
  }
  </style>
  