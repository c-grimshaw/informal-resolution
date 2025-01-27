import { auth } from "$lib/stores/authStore.svelte";

export const prerender = false;
export const ssr = false;
export const trailingSlash = 'never';

export const load = async ({ fetch }) => {
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
        auth.setToken(savedToken);
        await auth.loadUser(fetch);
        while (auth.loading) {
            await new Promise(resolve => setTimeout(resolve, 10));
        }
    }
    return {};
};