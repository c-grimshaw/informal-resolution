import { auth } from '../stores/authStore.svelte';

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

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
    const url = `${API_URL}${endpoint}`;
    const headers = new Headers({
        'Content-Type': 'application/json',
        ...options.headers,
    });
    
    if (auth.token) {
        headers.append('Authorization', `Bearer ${auth.token}`);
    }

    const config = {
        ...options,
        headers,
    };

    // Only stringify the body if it's not already a URLSearchParams and skipJsonStringify is not set
    if (config.body && !(config.body instanceof URLSearchParams) && !options.skipJsonStringify) {
        config.body = JSON.stringify(config.body);
    }

    const response = await fetch(url, config);
    return handleResponse(response);
}

export async function get(endpoint) {
    return request(endpoint);
}

export async function post(endpoint, data, options = {}) {
    return request(endpoint, {
        method: 'POST',
        body: data,
        ...options
    });
}

export async function put(endpoint, data, options = {}) {
    return request(endpoint, {
        method: 'PUT',
        body: data,
        ...options
    });
}

export async function patch(endpoint, data, options = {}) {
    return request(endpoint, {
        method: 'PATCH',
        body: data,
        ...options
    });
}

export async function del(endpoint) {
    return request(endpoint, {
        method: 'DELETE',
    });
} 