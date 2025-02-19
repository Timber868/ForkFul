<template>
  <div class="container">
    <div class="form-wrapper">
      <h1 class="title">Create Recipe</h1>
      <p class="subtitle">Share your culinary masterpiece with the world</p>

      <form @submit.prevent="submitRecipe" class="form-container">
        <label>Recipe Name</label>
        <input type="text" v-model="recipe.name" placeholder="Enter recipe name" required />

        <label>Posted Date</label>
        <input type="date" v-model="recipe.posted_date" required />

        <label>Username</label>
        <input type="text" v-model="recipe.username" placeholder="Your username" required />

        <label>Ingredients</label>
        <textarea v-model="recipe.ingredients" placeholder="Enter ingredients (one per line)" required></textarea>

        <label>Description</label>
        <textarea v-model="recipe.description" placeholder="Describe your recipe" required></textarea>

        <label>Recipe Image</label>
        <input type="file" @change="handleImageUpload" accept="image/png, image/jpeg, image/gif" />
        <img v-if="imagePreview" :src="imagePreview" class="preview-image" />

        <div class="button-container">
          <button type="submit" class="btn submit-btn">Submit Recipe</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recipe: this.getEmptyRecipe(),
      imageFile: null,
      imagePreview: null
    };
  },
  methods: {
    getEmptyRecipe() {
      return {
        name: '',
        posted_date: new Date().toISOString().split('T')[0],
        username: '',
        ingredients: '',
        description: ''
      };
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.imageFile = file;
        this.imagePreview = URL.createObjectURL(file);
      }
    },
    async submitRecipe() {
      const formData = new FormData();
      formData.append("name", this.recipe.name);
      formData.append("posted_date", this.recipe.posted_date);
      formData.append("username", this.recipe.username);
      formData.append("ingredients", this.recipe.ingredients);
      formData.append("description", this.recipe.description);
      
      if (this.imageFile) {
          formData.append("image", this.imageFile);
      }

      try {
          const response = await fetch("http://127.0.0.1:5000/recipes/", {
              method: "POST",
              body: formData
          });

          const data = await response.json();
          if (response.ok) {
              alert("Your recipe has been posted!");
              this.resetForm();
          } else {
              alert("Error: " + data.error);
          }
      } catch (error) {
          console.error("Error posting recipe:", error);
      }
    },
    resetForm() {
      this.recipe = this.getEmptyRecipe();
      this.imageFile = null;
      this.imagePreview = null;
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 90vh;
  padding: 1rem;
  background: rgba(210, 225, 204, 0.4);
  backdrop-filter: blur(10px);
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 500px;
  background: rgba(210, 225, 204, 0.4);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border: 1px solid #114538;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #114538;
  text-align: center;
}

.subtitle {
  font-size: 16px;
  color: #0f444c;
  margin-bottom: 20px;
  text-align: center;
}

.form-container {
  width: 100%;
}

input, textarea {
  width: 100%;
  padding: 0.75rem 0;
  border: none;
  border-bottom: 2px solid #0f444c;
  background: transparent;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus, textarea:focus {
  border-bottom-color: #5e8d83;
  box-shadow: 0 2px 0 0 #5e8d83;
}

.preview-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  margin-top: 10px;
  border-radius: 5px;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.submit-btn {
  background-color: #5e8d83;
  color: #d2e1cc;
}

.submit-btn:hover {
  background-color: #114538;
}
</style>


  
  