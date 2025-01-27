import { store } from "$lib/stores/store.svelte";
import { auth } from "$lib/stores/authStore.svelte";

export const load = async ({ fetch, parent }) => {
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
        const response = await fetch('/grievances', {
            headers: {
                'Authorization': `Bearer ${auth.token}`
            }
        });
        const grievances = await response.json();
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