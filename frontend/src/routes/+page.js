import { redirect } from '@sveltejs/kit';
import { auth } from '$lib/stores/authStore.svelte';

export const load = async () => {
	if (auth.isAuthenticated) {
		throw redirect(307, '/help');
	}
	
	return {};
};