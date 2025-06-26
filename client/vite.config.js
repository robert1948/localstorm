import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import { cacheBusterPlugin } from './vite.plugins.cachebuster.js'; // 👈 Import as named export

export default defineConfig({
  plugins: [
    react(),
    tsconfigPaths(),
    cacheBusterPlugin(), // 👈 Use the plugin as a function
  ],
  base: './', // ✅ Ensures relative paths for static assets after build
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''),
      },
    },
  },
});
