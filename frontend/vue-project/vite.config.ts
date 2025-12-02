/**
 * Vite configuration file for the Vue.js frontend application.
 *
 * This file defines how Vite should build, serve, and optimize the frontend.
 * It includes plugin configurations, path aliases, and development server settings
 * like API proxying to the backend.
 */

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(), // Official plugin for Vue 3 SFCs.
    vueJsx(), // Plugin for Vue JSX support.
    vueDevTools(), // Plugin for Vue DevTools integration in development.
  ],
  resolve: {
    alias: {
      // Configure path alias '@' to point to the 'src' directory.
      // This allows for cleaner import paths like `@/components/MyComponent.vue`.
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    // Configure a proxy for API requests during development.
    // This helps to bypass CORS issues by forwarding requests from the frontend
    // to the backend API server.
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // The address of your Flask backend API.
        changeOrigin: true, // Changes the origin of the host header to the target URL.
        // The rewrite rule is intentionally removed here to pass the /api prefix
        // directly to the Flask backend, which expects it.
      }
    }
  }
})
