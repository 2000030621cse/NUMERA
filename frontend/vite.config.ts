import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Forward health checks straight to the FastAPI backend
      "/health": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      // Forward API routes (e.g. /api/numerology/...) without rewriting the path
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
