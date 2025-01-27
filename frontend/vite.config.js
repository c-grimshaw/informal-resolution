import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: '0.0.0.0',
		port: 5173,
		strictPort: true,
		proxy: {
			'/users': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true
			},
			'/auth': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true
			},
			'/grievances': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true
			},
			'/stakeholders': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true
			}
		}
	}
});
