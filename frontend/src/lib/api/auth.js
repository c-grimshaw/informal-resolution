import { post, get } from './client';
import { auth } from '../stores/authStore.svelte';

export async function login(email, password) {
    try {
        // Create form data
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        // Use our post function with the correct headers
        const data = await post('/auth/jwt/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            skipJsonStringify: true
        });

        auth.setToken(data.access_token);
        
        // Fetch user data after successful login
        const userData = await get('/users/me');
        auth.setUser(userData);

        return data;
    } catch (error) {
        auth.logout();
        throw error;
    }
}

export async function register(email, password) {
    try {
        await post('/auth/register', {
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