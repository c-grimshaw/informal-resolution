let isAuthenticated = $state(false);
let isSupervisor = $state(false);
let isAdmin = $state(false);
let token = $state(null);
let user = $state(null);

function setToken(newToken) {
    token = newToken;
    if (newToken) {
        localStorage.setItem('token', newToken);
        isAuthenticated = true;
    } else {
        localStorage.removeItem('token');
        isAuthenticated = false;
    }
}

function setUser(userData) {
    user = userData;
    if (userData) {
        // Check both superuser status and role for admin privileges
        isAdmin = userData.is_superuser || userData.role === 'admin' || false;
        // Check superuser, admin role, or supervisor role for supervisor privileges
        isSupervisor = userData.is_superuser || userData.role === 'admin' || userData.role === 'supervisor' || false;
    } else {
        isAdmin = false;
        isSupervisor = false;
    }
}

function initialize() {
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
        setToken(savedToken);
    }
}

function logout() {
    setToken(null);
    setUser(null);
    isAdmin = false;
    isSupervisor = false;
    isAuthenticated = false;
}

export const auth = {
    get isAuthenticated() { return isAuthenticated; },
    get isSupervisor() { return isSupervisor; },
    get isAdmin() { return isAdmin; },
    get token() { return token; },
    get user() { return user; },
    setToken,
    setUser,
    initialize,
    logout
}; 