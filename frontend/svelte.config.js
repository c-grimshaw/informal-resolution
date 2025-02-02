import adapter from "@sveltejs/adapter-node";

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		output: {
			bundleStrategy: 'single'
		},
		prerender: {
			entries: [],
			handleHttpError: 'warn'
		},
		paths: {
			base: ''
		},
		appDir: '_app',
		csrf: {
			checkOrigin: false
		}
	}
};

export default config;
