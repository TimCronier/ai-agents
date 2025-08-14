// frontend/vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Toutes les requêtes commençant par /api vont à Django :
      "/api": "http://localhost:8000",
    },
    port: 5173,              // par défaut
  },
});
