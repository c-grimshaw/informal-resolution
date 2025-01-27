function createPersonalGrievancesStore() {
    const state = $state({
        grievances: [],
        loading: false,
        error: null
    });

    return {
        get grievances() { return state.grievances; },
        get loading() { return state.loading; },
        get error() { return state.error; },

        setGrievances(grievances) {
            state.grievances = grievances;
        },

        setLoading(value) {
            state.loading = value;
        },

        setError(error) {
            state.error = error;
        },

        deleteGrievance(id) {
            state.grievances = state.grievances.filter(g => g.id !== id);
        }
    };
}

export const personalGrievances = createPersonalGrievancesStore(); 