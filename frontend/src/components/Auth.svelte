<script>
    import { auth } from '../lib/stores/authStore.svelte';
    import { login, register, logout } from '../lib/api/auth';
    import { store } from '../lib/stores/store.svelte';
    import { scale } from 'svelte/transition';

    let email = $state('');
    let password = $state('');
    let isRegistering = $state(false);
    let loading = $state(false);

    async function handleSubmit(e) {
        e.preventDefault();
        store.setLoading(true);
        try {
            if (isRegistering) {
                await register(email, password);
                isRegistering = false;
            } else {
                await login(email, password);
            }
            email = '';
            password = '';
        } catch (e) {
            store.setError(e.message);
        } finally {
            loading = false;
        }
    }

    function handleLogout() {
        logout();
    }
</script>

{#if auth.isAuthenticated}
    <div class="auth-status">
        <span class="user-email" in:scale={{duration: 150, start: 0.95}}>{auth.user?.email}</span>
        <button class="logout-btn" onclick={handleLogout}>Logout</button>
    </div>
{:else}
    <form onsubmit={handleSubmit} class="auth-form">
        <div class="form-group">
            <input
                type="email"
                placeholder="Email"
                bind:value={email}
                required
            />
        </div>
        <div class="form-group">
            <input
                type="password"
                placeholder="Password"
                bind:value={password}
                required
            />
        </div>
        <div class="form-actions">
            <button type="submit" disabled={loading}>
                {#if loading}
                    Loading...
                {:else}
                    {isRegistering ? 'Register' : 'Login'}
                {/if}
            </button>
            <button
                type="button"
                class="switch-btn"
                onclick={() => (isRegistering = !isRegistering)}
            >
                {isRegistering ? 'Switch to Login' : 'Switch to Register'}
            </button>
        </div>
    </form>
{/if}

<style>
    .auth-form {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        max-width: 100%;
    }

    .form-group {
        margin: 0;
        width: 100%;
    }

    .form-group input {
        width: 150px;
        padding: 0.25rem 0.5rem;
        font-size: 0.9rem;
        border-radius: 4px;
        border: 1px solid #ccc;
    }

    .form-actions {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .auth-status {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
        max-width: 100%;
    }

    .user-email {
        color: #e0e0e0;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        min-width: 0;
        transition: all 0.2s ease;
        position: relative;
    }

    .user-email:hover {
        color: #C8102E;
        transform: scale(1.05);
    }

    .user-email::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(200, 16, 46, 0.1);
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }

    .user-email:hover::before {
        transform: translateX(0);
    }

    .logout-btn {
        background: #ff5252;
        color: white;
        white-space: nowrap;
    }

    .switch-btn {
        background: transparent;
        border: 1px solid #64b5f6;
        color: #64b5f6;
        white-space: nowrap;
    }

    button {
        padding: 0.25rem 0.5rem;
        font-size: 0.9rem;
        border-radius: 4px;
        min-width: 80px;
    }

    /* Tablet breakpoint */
    @media (max-width: 1024px) {
        .form-group input {
            width: 130px;
        }
    }

    /* Mobile breakpoint */
    @media (max-width: 768px) {
        .auth-form {
            flex-direction: column;
            width: 100%;
            gap: 0.75rem;
        }

        .form-group {
            width: 100%;
        }

        .form-group input {
            width: 100%;
            padding: 0.5rem;
        }

        .form-actions {
            width: 100%;
            justify-content: stretch;
        }

        button {
            flex: 1;
            padding: 0.5rem;
        }

        .auth-status {
            width: 100%;
            justify-content: space-between;
            padding: 0.5rem 0;
        }
    }

    /* Small mobile breakpoint */
    @media (max-width: 480px) {
        .form-actions {
            flex-direction: column;
        }

        .auth-status {
            flex-direction: column;
            gap: 0.5rem;
            align-items: stretch;
            text-align: center;
        }

        button {
            width: 100%;
        }
    }
</style> 