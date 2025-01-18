function createStore() {
    const state = $state({
        grievances: [],
        stakeholders: [],
        loading: false,
        error: null,
        successMessage: null
    });

    return {
        // Getters
        get grievances() { return state.grievances; },
        get stakeholders() { return state.stakeholders; },
        get loading() { return state.loading; },
        get error() { return state.error; },
        get successMessage() { return state.successMessage; },

        // Actions
        setGrievances(data) {
            state.grievances = data;
        },
        addGrievance(grievance) {
            state.grievances = [...state.grievances, grievance];
        },
        updateGrievance(id, updatedGrievance) {
            state.grievances = state.grievances.map(item => 
                item.id === id ? updatedGrievance : item
            );
        },
        deleteGrievance(id) {
            state.grievances = state.grievances.filter(item => item.id !== id);
        },

        // Stakeholders
        setStakeholders(data) {
            state.stakeholders = data;
        },
        addStakeholder(stakeholder) {
            state.stakeholders = [...state.stakeholders, stakeholder];
        },
        updateStakeholder(id, updatedStakeholder) {
            state.stakeholders = state.stakeholders.map(item => 
                item.id === id ? updatedStakeholder : item
            );
        },
        deleteStakeholder(id) {
            state.stakeholders = state.stakeholders.filter(item => item.id !== id);
        },

        // UI State
        setLoading(value) {
            state.loading = value;
        },
        setError(message) {
            state.error = message;
        },
        clearError() {
            state.error = null;
        },
        setSuccessMessage(message) {
            state.successMessage = message;
        },
        clearSuccessMessage() {
            state.successMessage = null;
        }
    };
}

export const store = createStore();