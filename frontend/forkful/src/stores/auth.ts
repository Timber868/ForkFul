import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
    const token = ref(localStorage.getItem("token") || null);
    const username = ref(localStorage.getItem("username") || null);
    const isAuthenticated = ref(!!token.value);

    const setToken = (newToken: string, user: string) => {
        token.value = newToken;
        isAuthenticated.value = true;
        localStorage.setItem("token", newToken);
        localStorage.setItem("username", user);
    };

    const logout = () => {
        username.value = null;
        token.value = null;
        isAuthenticated.value = false;
        localStorage.removeItem("token");
    };

    return { token, isAuthenticated, username, setToken, logout };
});