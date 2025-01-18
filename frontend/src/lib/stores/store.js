import { writable } from 'svelte/store';

// Create stores with initial values
export const grievances = writable([]);
export const stakeholders = writable([]);
export const loading = writable(false);
export const error = writable(null);

// Store actions
export const actions = {
    // Grievances
    setGrievances: (data) => grievances.set(data),
    addGrievance: (grievance) => {
        grievances.update($grievances => [...$grievances, grievance]);
    },
    updateGrievance: (id, updatedGrievance) => {
        grievances.update($grievances => 
            $grievances.map(item => item.id === id ? updatedGrievance : item)
        );
    },
    deleteGrievance: (id) => {
        grievances.update($grievances => $grievances.filter(item => item.id !== id));
    },

    // Stakeholders
    setStakeholders: (data) => stakeholders.set(data),
    addStakeholder: (stakeholder) => {
        stakeholders.update($stakeholders => [...$stakeholders, stakeholder]);
    },
    updateStakeholder: (id, updatedStakeholder) => {
        stakeholders.update($stakeholders => 
            $stakeholders.map(item => item.id === id ? updatedStakeholder : item)
        );
    },
    deleteStakeholder: (id) => {
        stakeholders.update($stakeholders => $stakeholders.filter(item => item.id !== id));
    },

    // UI State
    setLoading: (state) => loading.set(state),
    setError: (message) => error.set(message),
    clearError: () => error.set(null)
}; 