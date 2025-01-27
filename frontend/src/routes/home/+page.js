import { auth } from "$lib/stores/authStore.svelte";
import { personalGrievances } from "$lib/stores/personalGrievances.svelte.js";

export const load = async ({ fetch, parent }) => {
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
        const response = await fetch(`/grievances/user/${auth.user.id}`, {
            headers: {
                'Authorization': `Bearer ${auth.token}`
            }
        });
        const grievances = await response.json();
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