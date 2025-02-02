import { redirect } from '@sveltejs/kit';
import { auth } from '$lib/stores/authStore.svelte';
import { get } from '$lib/api/client';
import { store } from '$lib/stores/store.svelte';

export const load = async () => {
	if (auth.isAuthenticated) {
		try {
			store.setLoading(true);
			const [stakeholdersData, grievancesData, userData] = await Promise.all([
				get("/users/all"),
				get("/grievances"),
				get("/users/me")
			]);
			store.setStakeholders(stakeholdersData);
			store.setGrievances(grievancesData);
			auth.setUser(userData);
			throw redirect(307, '/help');
		} catch (e) {
			if (e instanceof Response && e.status === 307) {
				throw e;
			}
			store.setError(e.message);
			console.error("Failed to load initial data:", e);
		} finally {
			store.setLoading(false);
		}
	}
	
	return {};
};