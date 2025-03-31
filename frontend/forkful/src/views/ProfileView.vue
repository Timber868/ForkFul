<template>
    <div class="container">
        <div class="profile-info">
            <p class="title profile-title">Profile of '{{ user.username }}'</p>
            <div class="info">
                <label for="name">Name:</label>
                <span class="profile-field">{{ user.name }}</span>
            </div>
            <div class="info">
                <label for="card-number">Username:</label>
                <span class="profile-field">{{ user.username }}</span>
            </div>
            <div class="info">
                <label for="expiry-date">Email:</label>
                <span class="profile-field">{{ user.email }}</span>
            </div>
            <div class="info">
                <label for="cvv">Phone Number:</label>
                <span class="profile-field">{{ user.phoneNumber }}</span>
            </div>
        
        <!-- Dynamic List of Recipes -->
        <div class="items-container">
            <p class="items-title">Recipes</p>
            <div class="items-list">
                <div v-for="(recipe, index) in recipes" :key="index" class="item">
                    <div class="card-header">
                        <span class="card-title">{{ recipe.name }}</span>
                        <span class="card-username">{{ recipe.username }} </span>
                    </div>

                    <div class="card-information">
                        <img src="../assets/pasta-tim-test.jpg" alt="Recipe Image" />
                        <p class="card-description">
                            {{ recipe.description }}
                        </p>
                    </div>

                    <section class="ingredient-section">
                        <div
                        class="card-ingredients"
                        v-for="(ingredient, i) in recipe.ingredients.split('\r\n')"
                        :key="i"
                        >
                        {{ ingredient }}
                        </div>
                    </section>

                    <p class="card-date">{{ recipe.posted_date }}</p>
                </div>
            </div>
        </div>
    </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Define types
interface User {
    username: string;
    name: string;
    email: string;
    phoneNumber: string;
}

interface Recipe {
    id: number;
    name: string;
    posted_date: string;
    username: string;
    ingredients: string;
    description: string;
    image?: string; // Image might be optional
}

const user = ref<User>({
    username: '',
    name: '',
    email: '',
    phoneNumber: ''
});

const recipes = ref<Recipe[]>([]);

const username = 'admin';

onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/profile/${username}`);
        
        // Assuming response contains the user and recipes
        user.value = response.data.user;

        // Update recipes to match the correct fields
        recipes.value = response.data.recipes.map((recipe: any) => ({
            id: recipe.id,
            name: recipe.name,
            posted_date: recipe.posted_date,
            username: recipe.username,
            ingredients: recipe.ingredients,
            description: recipe.description,
            image: recipe.image
        }));
    } catch (error) {
        console.error("There was an error fetching the data:", error);
    }
});
</script>

<style scoped>
/* General Container Styling */
.container {
    display: flex;
    justify-content: center;
    padding-top: 50px;
}

.profile-info {
    width: 80%;
    max-width: 800px;
    padding: 30px;
    background-color: #d2e1cc;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    text-align: center;
}

/* Profile Title */
.profile-title {
    font-size: 1.75rem;
    font-weight: bold;
    color: #0f444c; /* Primary color */
    padding-bottom: 20px;
}

/* Info Section */
.info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    font-size: 1.2rem;
}

.info label {
    font-weight: bold;
    color: #114538; /* Accent color */
    padding-left: 30px;
    width: 40%;
    text-align: right;
}

.profile-field {
    color: #5e8d83; /* Light Green for the fields */
    padding-right: 30px;
    width: 40%;
}

/* Recipe Section */
.items-container {
    margin-top: 30px;
    padding: 20px;
    background: #5e8d83; /* Light Green */
    border-radius: 8px;
}

.items-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #fff; /* White text */
    margin-bottom: 15px;
    text-align: center;
}

.items-list {
    list-style-type: none;
    padding: 0;
}

/* Individual Recipe Item */
.item {
    padding: 15px;
    border-bottom: 1px solid #0f444c; /* Primary color as border */
    background-color: #ffffff;
    margin-bottom: 10px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.item:last-child {
    border-bottom: none;
}

/* Recipe Card Header */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 1.2rem;
    color: #114538; /* Accent color */
    font-weight: bold;
}

/* Recipe Image */
.card-information img {
    max-width: 100%;
    border-radius: 8px;
    margin-top: 15px;
}

/* Description */
.card-description {
    font-size: 1rem;
    color: #161d23; /* Dark text for description */
    margin-top: 10px;
}

/* Ingredients Section */
.ingredient-section {
    margin-top: 15px;
}

.card-ingredients {
    font-size: 0.95rem;
    color: #0f444c;
    margin-bottom: 5px;
}

/* Date */
.card-date {
    font-size: 0.9rem;
    color: #114538; /* Accent color */
    margin-top: 10px;
    font-style: italic;
}
</style>
