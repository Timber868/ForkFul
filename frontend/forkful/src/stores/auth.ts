import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
    const token = ref(localStorage.getItem("token") || null);
    const isAuthenticated = ref(!!token.value);

    const setToken = (newToken: string) => {
        token.value = newToken;
        isAuthenticated.value = true;
        localStorage.setItem("token", newToken);
    };

    const logout = () => {
        token.value = null;
        isAuthenticated.value = false;
        localStorage.removeItem("token");
    };

    return { token, isAuthenticated, setToken, logout };
});