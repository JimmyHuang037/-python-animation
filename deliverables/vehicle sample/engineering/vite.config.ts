import {defineConfig} from 'vite';
import motionCanvas from '@motion-canvas/vite-plugin';
export default defineConfig({plugins:[(motionCanvas as any).default({project:'./src/full-project-v1.ts'})],server:{host:'0.0.0.0',port:9031,strictPort:true},build:{rollupOptions:{input:'full-v1.html'}}});
