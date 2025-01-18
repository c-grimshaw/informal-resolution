import { auth } from '../stores/authStore.svelte';

const BASE_URL = 'http://127.0.0.1:8000';

async function handleResponse(response) {
    if (!response.ok) {
        const error = await response.text();
        throw new Error(error || response.statusText);
    }
    return response.json();
}

export async function get(endpoint) {
    const headers = {};
    if (auth.token) {
        headers['Authorization'] = `Bearer ${auth.token}`;
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, { headers });
    return handleResponse(response);
}

export async function post(endpoint, data) {
    const headers = {
        'Content-Type': 'application/json',
    };
    if (auth.token) {
        headers['Authorization'] = `Bearer ${auth.token}`;
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
    });
    return handleResponse(response);
}

export async function put(endpoint, data) {
    const headers = {
        'Content-Type': 'application/json',
    };
    if (auth.token) {
        headers['Authorization'] = `Bearer ${auth.token}`;
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data)
    });
    return handleResponse(response);
}

export async function del(endpoint) {
    const headers = {};
    if (auth.token) {
        headers['Authorization'] = `Bearer ${auth.token}`;
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'DELETE',
        headers
    });
    return handleResponse(response);
} 