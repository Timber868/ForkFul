<template>
    <div class="feed-container">
        <div class ="feed-body">
            <div class="feed-recipes">
                <h2 class="recipe-name">Recipe name</h2>

                <div class="recipe-header">
                    <p class="posted-date"></p>
                    <p class="username"></p>
                </div>

                <div class="content-block">
                    <img src="" alt="Recipe image" class="recipe-image">
                    <p class="recipe-description"></p>
                </div>

                <div class="recipe-ingredients"></div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts"></script>

<style scoped>
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

</style>