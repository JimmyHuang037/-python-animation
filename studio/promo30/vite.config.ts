import {defineConfig} from 'vite';
import motionCanvas from '@motion-canvas/vite-plugin';
export default defineConfig({plugins:[(motionCanvas as any).default()],server:{host:'127.0.0.1',port:9030}});
