import adapter from '@sveltejs/adapter-node'; // <-- AANGEPAST
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter() // <-- AANGEPAST
    }
};

export default config;