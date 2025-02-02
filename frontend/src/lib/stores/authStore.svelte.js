import { get } from '../api/client';
import { browser } from '$app/environment';

function createAuthStore() {
    const state = $state({
        user: null,
        isAdmin: false,
        isSupervisor: false,
        loading: false,
        token: null,
        isAuthenticated: false,
        currentRoute: 'help'
    });

    return {
        get user() { return state.user; },
        get isAdmin() { return state.isAdmin; },
        get isSupervisor() { return state.isSupervisor; },
        get loading() { return state.loading; },
        get token() { return state.token; },
        get isAuthenticated() { return state.isAuthenticated; },
        get currentRoute() { return state.currentRoute; },

        setToken(newToken) {
            state.token = newToken;
            if (newToken) {
                if (browser) {
                    localStorage.setItem('token', newToken);
                }
                state.isAuthenticated = true;
            } else {
                if (browser) {
                    localStorage.removeItem('token');
                }
                state.isAuthenticated = false;
                state.user = null;
                state.isAdmin = false;
                state.isSupervisor = false;
            }
        },

        setUser(userData) {
            state.user = userData;
            if (userData) {
                state.isAdmin = userData.is_superuser || userData.role === 'admin';
                state.isSupervisor = userData.is_superuser || userData.role === 'admin' || userData.role === 'supervisor';
                state.currentRoute = 'help';
            } else {
                state.isAdmin = false;
                state.isSupervisor = false;
            }
        },

        setLoading(value) {
            state.loading = value;
        },

        async loadUser() {
            state.loading = true;
            try {
                const userData = await get('/users/me');
                this.setUser(userData);
            } catch (error) {
                console.error('Failed to load user:', error);
                this.setToken(null);
            } finally {
                state.loading = false;
            }
        },

        async initialize() {
            state.loading = true;
            if (browser) {
                const savedToken = localStorage.getItem('token');
                if (savedToken) {
                    this.setToken(savedToken);
                    await this.loadUser();
                }
            }
            state.loading = false;
        },

        logout() {
            state.user = null;
            state.isAdmin = false;
            state.isSupervisor = false;
            state.isAuthenticated = false;
            state.token = null;
            if (browser) {
                localStorage.removeItem('token');
            }
            state.currentRoute = 'login';
        }
    };
}

export const auth = createAuthStore();