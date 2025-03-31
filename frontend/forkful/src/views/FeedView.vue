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
                {{ recipe.description }}
            </p>
            <!-- <p class="description">Description: {{ recipe.description }}</p> -->
          </div>

          <section class="ingredient-section">
            <div
              class="card-ingredients"
              v-for="(ingredient, index) in recipe.ingredients.split('\r\n')"
              :key="index"
            >
              {{ ingredient }}
            </div>
          </section>

          <div class="reactions">
            <div class="reaction-item">
              <span v-if="recipe.reactions">{{ recipe.reactions.booms }}</span>
              <img src="../assets/boom.png" height="30px" alt="Boom" />
            </div>
            <div class="reaction-item">
              <span v-if="recipe.reactions">{{ recipe.reactions.dooms }}</span>
              <img src="../assets/doom.png" height="30px" alt="Doom" />
            </div>
          </div>

          <p class="card-date">{{ recipe.posted_date }}</p>
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

  try {
    for (const recipe of recipes.value) {
      try {
        const reactionResponse = await axios.get(`http://127.0.0.1:5000/reactions?recipe_id=${recipe.id}&user_id=1`);
        recipe.reactions = reactionResponse.data;
      } catch (reactionError) {
        console.error(`Error fetching reactions for recipe ${recipe.id}:`, reactionError);
      }
    }
  }
  catch (error) {
    console.error("Error fetching reactions:", error);
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

.feed::-webkit-scrollbar {
  display: none;
}


.recipe-card {
  padding: 1rem;
  /* You can remove the border or make it lighter */
  border: 1px solid #d2e1cc; 
  border-radius: 4px;
  background-color: #d2e1cc; /* A clean white background can be nice */

  /* A subtle shadow to lift the card off the page */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}


/* ==================== Header ==================== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem; /* extra space below header */
  border-bottom: 1px solid #993232; /* a subtle separator */
}

.card-title {
  font-size: 1.5rem; /* Large enough to be eye-catching */
  font-weight: bold;
  margin: 0;
}

.card-username {
  font-size: 1rem;
  color: #666; /* A bit more subdued than the title */
}


/* ==================== Information ==================== */

.card-information {
  display: flex;
  flex-direction: row;
  gap: 2rem;

  margin-bottom: 2em;
}

.recipe-card img {
  width: 30em;
  height: auto;
}

.card-description {
  font-size: 1.5rem;
  line-height: 1.5;
  color: #333;
}


/* ==================== Ingredient section ==================== */

.ingredient-section {
  display: grid;
  /* Each column is at least 120px; adjust as needed */
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem; /* Space between items */
}

.card-ingredients {
  background-color: #5e8d83;
  padding: 0.5rem;
  text-align: center;
  border-radius: 4px;
}

/* ==================== Posted Date ==================== */
.card-date {
  margin: 0.5rem 0;
  color: #555;
  font-size: 0.9rem;
}

/* ==================== Reactions ==================== */
.reactions {
  display: flex;
  margin-top: 1rem;
  gap: 1rem;
}
.reaction-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}
.reaction-item span {
  font-size: 1.2rem;
  color: #333;
  font-weight: bold;
  transition: color 0.2s;
}
.reaction-item img {
  width: 50px;
  height: auto;
  transition: transform 0.2s;
}
.reaction-item img:hover {
  transform: scale(1.1);
}


</style>
