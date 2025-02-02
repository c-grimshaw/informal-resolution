import { auth } from "$lib/stores/authStore.svelte";
import { personalGrievances } from "$lib/stores/personalGrievances.svelte.js";
import { get } from "$lib/api/client";

export const load = async ({ parent }) => {
    // Wait for parent layout load to complete
    await parent();
    
    // Wait for any auth loading to complete
    while (auth.loading) {
        await new Promise(resolve => setTimeout(resolve, 10));
    }

    if (!auth.user?.id) {
        personalGrievances.setGrievances([]);
        return { grievances: [] };
    }

    try {
        personalGrievances.setLoading(true);
        const grievances = await get(`/grievances/user/${auth.user.id}`);
        personalGrievances.setGrievances(grievances);
        return { grievances };
    } catch (error) {
        console.error("Failed to load user grievances:", error);
        personalGrievances.setError("Failed to load grievances");
        personalGrievances.setGrievances([]);
        return { grievances: [], error: "Failed to load grievances" };
    } finally {
        personalGrievances.setLoading(false);
    }
}; 