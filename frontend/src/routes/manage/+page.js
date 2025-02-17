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
        store.setGrievances([]);
        return { grievances: [] };
    }

    try {
        store.setLoading(true);
        const grievances = await get('/grievances');
        store.setGrievances(grievances);
        return { grievances };
    } catch (error) {
        console.error("Failed to load grievances:", error);
        store.setError("Failed to load grievances");
        store.setGrievances([]);
        return { grievances: [], error: "Failed to load grievances" };
    } finally {
        store.setLoading(false);
    }
}; 