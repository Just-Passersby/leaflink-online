import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/auth':   { target: 'http://127.0.0.1:8000', changeOrigin: true },
			'/notes':  { target: 'http://127.0.0.1:8000', changeOrigin: true },
			'/tags':   { target: 'http://127.0.0.1:8000', changeOrigin: true },
			'/vaults': { target: 'http://127.0.0.1:8000', changeOrigin: true },
			'/search': { target: 'http://127.0.0.1:8000', changeOrigin: true }
		}
	}
});
