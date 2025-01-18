<script>
    import { auth } from '../lib/stores/authStore.svelte';
    import { login, register, logout } from '../lib/api/auth';
    import { error as errorStore } from '../lib/stores/store';

    let email = $state('');
    let password = $state('');
    let isRegistering = $state(false);
    let loading = $state(false);

    async function handleSubmit(e) {
        e.preventDefault();
        loading = true;
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
            errorStore.set(e.message);
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
        <span>Logged in as {auth.user?.email}</span>
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
    }

    .form-group {
        margin: 0;
    }

    .form-group input {
        width: 150px;
        padding: 0.25rem 0.5rem;
        font-size: 0.9rem;
    }

    .form-actions {
        display: flex;
        gap: 0.5rem;
    }

    .auth-status {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: #e0e0e0;
    }

    .logout-btn {
        background: #ff5252;
        color: white;
    }

    .switch-btn {
        background: transparent;
        border: 1px solid #64b5f6;
        color: #64b5f6;
    }

    button {
        padding: 0.25rem 0.5rem;
        font-size: 0.9rem;
    }

    @media (max-width: 768px) {
        .auth-form {
            flex-direction: column;
            width: 100%;
        }

        .form-group input {
            width: 100%;
        }

        .form-actions {
            width: 100%;
            justify-content: stretch;
        }

        button {
            flex: 1;
        }
    }
</style> 