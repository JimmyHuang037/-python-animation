import {defineConfig} from 'vite';
import motionCanvas from '@motion-canvas/vite-plugin';

export default defineConfig({
  plugins: [(motionCanvas as any).default()],
  // Keep the editor plugin and UI on the same application context.
  optimizeDeps: {exclude: ['@motion-canvas/ui']},
  server: {host: '127.0.0.1', port: 9033, allowedHosts: ['motion40']},
});
