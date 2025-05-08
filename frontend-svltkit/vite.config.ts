import { sveltekit } from '@sveltejs/kit/vite';
import type { UserConfig } from 'vite';


const config: UserConfig = {
	plugins: [sveltekit()],
	optimizeDeps: {
		exclude: ['fsevents']
	},
	server: {
		proxy: {
			'^/(user|chat|character)': {
				target: 'http://localhost:8000',
				changeOrigin: true,
			}
		}
	}
};

export default config;
