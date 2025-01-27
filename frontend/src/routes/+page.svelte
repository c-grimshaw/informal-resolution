<script>
    import { auth } from "$lib/stores/authStore.svelte";
    import { get } from "$lib/api/client";
    import { store } from "$lib/stores/store.svelte";
    import { goto } from "$app/navigation";

    async function loadInitialData() {
        if (!auth.isAuthenticated) return;

        try {
            store.setLoading(true);
            const [stakeholdersData, grievancesData, userData] =
                await Promise.all([
                    get("/users/all"),
                    get("/grievances"),
                    get("/users/me"),
                ]);
            store.setStakeholders(stakeholdersData);
            store.setGrievances(grievancesData);
            auth.setUser(userData);
            goto('/help');
        } catch (e) {
            store.setError(e.message);
            console.error("Failed to load initial data:", e);
        } finally {
            store.setLoading(false);
        }
    }

    $effect(() => {
        if (auth.isAuthenticated) {
            loadInitialData();
        }
    });
</script>

<style>
    :global(body) {
        background-color: #1a1a1a;
        color: #e0e0e0;
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
            Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    :global(*) {
        box-sizing: border-box;
    }

    :global(.card) {
        background: #3d3d3d;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    :global(input),
    :global(textarea),
    :global(select) {
        background: #3d3d3d;
        border: 1px solid #4d4d4d;
        color: #e0e0e0;
        padding: 0.75rem;
        border-radius: 4px;
        width: 100%;
        font-size: 0.95rem;
    }

    :global(button) {
        background: #c8102e;
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.95rem;
        font-weight: 500;
    }

    :global(button:hover) {
        background: #e31837;
        transform: translateY(-1px);
    }

    :global(button:disabled) {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
