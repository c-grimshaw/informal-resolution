function createAuthStore() {
    // Create a state object to hold all mutable state
    const state = $state({
        token: '',
        user: {
            role: '',
            name: '',
            email: ''
        }
    });
    
    // Derived values using state object
    const role = $derived(state.user.role || '');
    const isAuthenticated = $derived(!!state.token);
    const isAdmin = $derived(role === 'admin');
    const isSupervisor = $derived(role === 'supervisor' || role === 'admin');
    
    return {
        get token() { return state.token; },
        get user() { return state.user; },
        get isAuthenticated() { return isAuthenticated; },
        get role() { return role; },
        get isAdmin() { return isAdmin; },
        get isSupervisor() { return isSupervisor; },
        
        setUser(userData) {
            if (!userData) {
                state.user = {
                    role: '',
                    name: '',
                    email: ''
                };
                localStorage.removeItem('user');
                return;
            }
            
            state.user = {
                role: userData.role || '',
                name: userData.name || '',
                email: userData.email || '',
                ...userData
            };
            localStorage.setItem('user', JSON.stringify(state.user));
        },

        setToken(newToken) {
            state.token = newToken || '';
            if (newToken) {
                localStorage.setItem('token', newToken);
            } else {
                localStorage.removeItem('token');
            }
        },

        handleLogin(userData, token) {
            this.setUser(userData);
            this.setToken(token);
        },

        initialize() {
            // Initialize with empty values
            state.token = '';
            state.user = {
                role: '',
                name: '',
                email: ''
            };
            
            // Restore token from localStorage
            const storedToken = localStorage.getItem('token');
            if (storedToken) {
                state.token = storedToken;
            }
            
            // Restore user data from localStorage
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                try {
                    const parsedUser = JSON.parse(storedUser);
                    state.user = {
                        role: parsedUser.role || '',
                        name: parsedUser.name || '',
                        email: parsedUser.email || '',
                        ...parsedUser
                    };
                } catch (e) {
                    console.error('Failed to parse stored user data:', e);
                    localStorage.removeItem('user');
                }
            }
        },

        logout() {
            state.token = '';
            state.user = {
                role: '',
                name: '',
                email: ''
            };
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        },

        hasRole(requiredRole) {
            if (!state.user.role) return false;
            if (requiredRole === 'admin') return role === 'admin';
            if (requiredRole === 'supervisor') return role === 'supervisor' || role === 'admin';
            return true;
        }
    };
}

export const auth = createAuthStore(); 