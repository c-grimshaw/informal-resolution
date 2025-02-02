import { store } from "$lib/stores/store.svelte";
import { auth } from "$lib/stores/authStore.svelte";
import { get } from "$lib/api/client";

export const load = async ({ parent }) => {
    // Wait for parent layout load to complete
    await parent();
    
    // Wait for any auth loading to complete
    while (auth.loading) {
        await new Promise(resolve => setTimeout(resolve, 10));
    }

    if (!auth.user?.id) {
        store.setStakeholders([]);
        return { stakeholders: [] };
    }

    try {
        store.setLoading(true);
        const stakeholders = await get('/users/all');
        store.setStakeholders(stakeholders);
        return { stakeholders };
    } catch (error) {
        console.error("Failed to load stakeholders:", error);
        store.setError("Failed to load stakeholders");
        store.setStakeholders([]);
        return { stakeholders: [], error: "Failed to load stakeholders" };
    } finally {
        store.setLoading(false);
    }
}; 