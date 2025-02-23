<template>
  <section class="feed-container">
    <div class="feed-body">
      <div class="feed">
        <div v-for="recipe in recipes" :key="recipe.id" class="recipe-card">
          <div class="card-header">
            <span class="card-title">{{ recipe.name }}</span>
            <span class="card-username">{{ recipe.username }} </span>
          </div>

          <div class="card-information">
            <!-- <img :src="recipe.image" alt="Recipe Image" /> -->
            <img src="../assets/pasta-tim-test.jpg" alt="Recipe Image" />
            <p class="card-description">
              Description: Lorem ipsum dolor sit amet, consectetur adipisicing
              elit. Suscipit dignissimos assumenda architecto tempore accusamus
              in dolores a. Corporis est rerum obcaecati distinctio perspiciatis
              fuga, illo, fugiat vel, sequi nulla explicabo?
            </p>
            <!-- <p class="description">Description: {{ recipe.description }}</p> -->
          </div>

          <p>Ingredients:</p>
          <div
            class="card-ingredients"
            v-for="(ingredient, index) in recipe.ingredients.split('\r\n')"
            :key="index"
          >
            {{ ingredient }}
          </div>
          <p>Posted on: {{ recipe.posted_date }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const recipes = ref<any[]>([]);

const fetchRecipes = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/recipes");
    recipes.value = response.data;
    console.log("Recipes fetched:", recipes.value);
  } catch (error) {
    console.error("Error fetching recipes:", error);
  }
};

onMounted(() => {
  fetchRecipes();
});
</script>

<style scoped>
.feed-body {
  background: rgba(210, 225, 204, 0.4);
  backdrop-filter: blur(40px);

  padding: 2rem;
  border: 1px solid #114538;

  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);

  max-width: 1200px;
  width: 100%;
}

.feed-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 90vh;
  padding: 1rem;
  background-image: url("../assets/feed-background.webp");
  background-size: cover;
  background-position: center;
}
.feed {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 90vh; /* adjust as needed */
  overflow-y: auto; /* allows scrolling */
}

.recipe-card {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* ==================== Header ==================== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: bold;
}

.card-title {
  font-size: 1.5rem;
}

/* ==================== Information ==================== */

.card-information {
  display: flex;
  flex-direction: row;
  gap: 2rem;
}

.recipe-card img {
  width: 20em;
  height: auto;
}

.card-description {
  font-size: 1.5rem;
}
</style>
