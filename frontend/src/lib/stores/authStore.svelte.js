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
        isAdmin = userData.is_superuser || false;
        // In FastAPI Users, superuser has all privileges
        isSupervisor = userData.is_superuser || userData.is_supervisor || false;
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