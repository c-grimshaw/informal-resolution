import { post } from './client';
import { auth } from '../stores/authStore.svelte';

export async function login(email, password) {
    try {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch('http://127.0.0.1:8000/auth/jwt/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();
        auth.setToken(data.access_token);
        
        // Fetch user data after successful login
        const userResponse = await fetch('http://127.0.0.1:8000/users/me', {
            headers: {
                'Authorization': `Bearer ${data.access_token}`
            }
        });
        
        if (userResponse.ok) {
            const userData = await userResponse.json();
            auth.setUser(userData);
        }

        return data;
    } catch (error) {
        auth.logout();
        throw error;
    }
}

export async function register(email, password) {
    try {
        const response = await post('/auth/register', {
            email,
            password,
            is_active: true,
            is_superuser: false,
            is_verified: false
        });
        
        // After registration, log the user in
        return await login(email, password);
    } catch (error) {
        auth.logout();
        throw error;
    }
}

export function logout() {
    auth.logout();
} 