import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // Import Pinia store
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import PostView from '@/views/PostView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    }, 
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView,
      meta: { requiresAuth: true } // Mark route as protected
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true } // Mark route as protected
    },
    {
      path: '/post',
      name: 'post',
      component: PostView,
      meta: { requiresAuth: true } // Mark route as protected
    }
  ],
})

// Global Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login'); // Redirect to login if not authenticated
  } else {
    next(); // Allow access
  }
});

export default router;