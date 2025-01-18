import { auth } from '../stores/authStore.svelte';

const BASE_URL = 'http://127.0.0.1:8000/auth';

export async function login(email, password) {
    const response = await fetch(`${BASE_URL}/jwt/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        },
        body: new URLSearchParams({
            username: email,
            password: password,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
    }

    const data = await response.json();
    auth.handleLogin({ email }, data.access_token);
    return data;
}

export async function register(email, password, role = 'user') {
    const response = await fetch(`${BASE_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            password,
            role,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
    }

    return await response.json();
}

export async function logout() {
    auth.logout();
} 