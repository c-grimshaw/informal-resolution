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

export async function get(endpoint) {
    const headers = new Headers();
    if (auth.token) {
        headers.append('Authorization', `Bearer ${auth.token}`);
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, { headers });
    return handleResponse(response);
}

export async function post(endpoint, data) {
    const headers = new Headers({
        'Content-Type': 'application/json'
    });
    if (auth.token) {
        headers.append('Authorization', `Bearer ${auth.token}`);
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
    });
    return handleResponse(response);
}

export async function put(endpoint, data) {
    const headers = new Headers({
        'Content-Type': 'application/json'
    });
    if (auth.token) {
        headers.append('Authorization', `Bearer ${auth.token}`);
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data)
    });
    return handleResponse(response);
}

export async function del(endpoint) {
    const headers = new Headers();
    if (auth.token) {
        headers.append('Authorization', `Bearer ${auth.token}`);
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'DELETE',
        headers
    });
    return handleResponse(response);
} 