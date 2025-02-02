import { auth } from "$lib/stores/authStore.svelte";
import { browser } from '$app/environment';

export const prerender = false;
export const ssr = false;
export const trailingSlash = 'never';

export const load = async () => {
    if (browser) {
        const savedToken = localStorage.getItem('token');
        if (savedToken) {
            auth.setToken(savedToken);
            await auth.loadUser();
            while (auth.loading) {
                await new Promise(resolve => setTimeout(resolve, 10));
            }
        }
    }
    return {};
};