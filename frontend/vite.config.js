import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/auth': 'http://127.0.0.1:8000',
			'/notes': 'http://127.0.0.1:8000',
			'/tags': 'http://127.0.0.1:8000',
			'/vaults': 'http://127.0.0.1:8000',
			'/search': 'http://127.0.0.1:8000'
		}
	}
});
