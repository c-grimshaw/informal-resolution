import { auth } from '../stores/authStore.svelte';

const BASE_URL = 'http://127.0.0.1:8000';

async function handleResponse(response) {
    if (!response.ok) {
        let errorMessage;
        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || response.statusText;
        } catch {
            errorMessage = await response.text() || response.statusText;
        }

        if (response.status === 401) {
            auth.logout();
            throw new Error('Your session has expired. Please log in again.');
        }
        throw new Error(errorMessage);
    }
    return response.json();
}

async function request(endpoint, options = {}) {
    const headers = new Headers({
        ...(options.body && { 'Content-Type': 'application/json' })
    });
    
    if (auth.token) {
        headers.append('Authorization', `Bearer ${auth.token}`);
    }

    const config = {
        ...options,
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    return handleResponse(response);
}

export const get = (endpoint) => request(endpoint);
export const post = (endpoint, data) => request(endpoint, { method: 'POST', body: data });
export const put = (endpoint, data) => request(endpoint, { method: 'PUT', body: data });
export const patch = (endpoint, data) => request(endpoint, { method: 'PATCH', body: data });
export const del = (endpoint) => request(endpoint, { method: 'DELETE' }); 