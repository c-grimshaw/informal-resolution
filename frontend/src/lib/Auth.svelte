<script>
    import { auth } from "$lib/stores/authStore.svelte";
    import { login, register, logout } from "$lib/api/auth";
    import { store } from "$lib/stores/store.svelte";
    import { scale } from "svelte/transition";
    import UserProfileModal from "$lib/UserProfileModal.svelte";

    let showProfileModal = $state(false);
    let email = $state("");
    let password = $state("");
    let isRegistering = $state(false);
    let loading = $state(false);
    let submitting = $state(false);

    async function handleSubmit(e) {
        e.preventDefault();
        submitting = true;
        store.setLoading(true);
        try {
            if (isRegistering) {
                await register(email, password);
                isRegistering = false;
            } else {
                await login(email, password);
            }
            email = "";
            password = "";
        } catch (e) {
            store.setError(e.message);
        } finally {
            loading = false;
            submitting = false;
            store.setLoading(false);
        }
    }

    async function handleLogout() {
        // Clear any form states from localStorage
        localStorage.removeItem("grievanceFormState");
        localStorage.removeItem("grievanceFormStep");
        await logout();
        window.location.href = '/';
    }
</script>

<div class="auth-container">
    {#if auth.loading}
        <div class="loading">Loading...</div>
    {:else if auth.isAuthenticated}
        <div class="user-info">
            <button
                class="user-button"
                onclick={() => (showProfileModal = true)}
            >
                <span in:scale={{ duration: 150, start: 0.95 }}>
                    {auth.user?.email || "User"}
                </span>
                {#if auth.user?.role && auth.user.role !== "user"}
                    <span class="role-badge {auth.user.role}">
                        {auth.user.role}
                    </span>
                {/if}
            </button>
            <button class="logout-button" onclick={handleLogout}>Logout</button>
        </div>
    {:else}
        <form class="login-form" onsubmit={handleSubmit}>
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
                <button
                    type="submit"
                    class="submit-button"
                    disabled={submitting}
                >
                    {submitting
                        ? "Loading..."
                        : isRegistering
                          ? "Register"
                          : "Login"}
                </button>
                <button
                    type="button"
                    class="switch-btn"
                    onclick={() => (isRegistering = !isRegistering)}
                >
                    {isRegistering ? "Switch to Login" : "Switch to Register"}
                </button>
            </div>
        </form>
    {/if}
</div>

<UserProfileModal
    isOpen={showProfileModal}
    closeModal={() => (showProfileModal = false)}
    onProfileUpdate={async () => {
        // Dispatch a custom event that can be listened to by parent components
        const event = new CustomEvent("profileUpdate");
        window.dispatchEvent(event);
    }}
/>

<style>
    .auth-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        justify-content: flex-end;
    }

    .user-button {
        background: none;
        border: none;
        color: var(--text-light, #ffffff);
        padding: 0.5rem;
        font-size: 0.9rem;
        cursor: pointer;
        border-radius: 4px;
        transition: all 0.2s;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
    }

    .user-button span {
        position: relative;
        z-index: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 200px;
    }

    .user-button:hover {
        color: #c8102e;
    }

    .user-button::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(200, 16, 46, 0.1);
        transform: translateX(-100%);
        transition: transform 0.3s ease;
        z-index: 0;
    }

    .user-button:hover::before {
        transform: translateX(0);
    }

    .logout-button {
        background: var(--primary-dark, #1a1a1a);
        border: 1px solid var(--gray-medium, #666666);
        color: var(--text-light, #ffffff);
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
    }

    .logout-button:hover {
        background: var(--gray-medium, #666666);
        transform: translateY(-1px);
    }

    .login-form {
        display: flex;
        align-items: center;
        background: var(--primary-dark, #1a1a1a);
        padding: 0.5rem;
        border-radius: 4px;
        gap: 0.5rem;
        width: 100%;
        justify-content: flex-end;
    }

    .form-group {
        margin: 0;
        position: relative;
        width: 140px;
    }

    .form-group input {
        width: 100%;
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        border-radius: 4px;
        background: var(--gray-dark, #333333);
        border: 1px solid var(--gray-medium, #666666);
        color: var(--text-light, #ffffff);
        transition: all 0.2s ease;
    }

    .form-group input:focus {
        outline: none;
        border-color: #c8102e;
        box-shadow: 0 0 0 2px rgba(200, 16, 46, 0.1);
    }

    .form-group input::placeholder {
        color: var(--gray-medium, #666666);
    }

    .form-actions {
        display: flex;
        gap: 0.5rem;
    }

    .submit-button {
        background: #c8102e;
        border: none;
        color: var(--text-light, #ffffff);
        padding: 0.5rem 1rem;
        font-weight: 500;
        min-width: 80px;
        transition: all 0.2s ease;
    }

    .submit-button:hover {
        background: #e31837;
        transform: translateY(-1px);
    }

    .submit-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none;
        background: var(--gray-medium, #666666);
    }

    .switch-btn {
        background: transparent;
        border: 1px solid #64b5f6;
        color: #64b5f6;
        white-space: nowrap;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .switch-btn:hover {
        background: rgba(100, 181, 246, 0.1);
        transform: translateY(-1px);
    }

    .role-badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75em;
        font-weight: 500;
        text-transform: capitalize;
        margin-left: 8px;
    }

    .role-badge.admin {
        background: rgba(244, 67, 54, 0.2);
        color: #f44336;
        border: 1px solid #f44336;
    }

    .role-badge.supervisor {
        background: rgba(33, 150, 243, 0.2);
        color: #2196f3;
        border: 1px solid #2196f3;
    }

    .role-badge.user {
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
        border: 1px solid #4caf50;
    }

    /* Mobile breakpoint */
    @media (max-width: 768px) {
        .auth-container {
            padding: 0.5rem;
            background: var(--primary-dark, #1a1a1a);
            border-radius: 4px;
        }

        .user-info {
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .user-button {
            padding: 0.75rem;
            font-size: 1rem;
        }

        .user-button span {
            max-width: 150px;
        }

        .logout-button {
            padding: 0.75rem;
            font-size: 1rem;
        }

        .login-form {
            flex-direction: column;
            gap: 0.75rem;
            padding: 0.75rem;
            justify-content: stretch;
        }

        .form-group {
            width: 100%;
        }

        .form-group input {
            width: 100%;
            padding: 0.75rem;
            font-size: 1rem;
        }

        .form-actions {
            width: 100%;
            gap: 0.75rem;
        }

        button {
            padding: 0.75rem;
            font-size: 1rem;
            justify-content: center;
        }
    }

    /* Small mobile breakpoint */
    @media (max-width: 480px) {
        .auth-container {
            padding: 0.75rem;
        }

        .form-actions {
            flex-direction: column;
        }

        .user-button span {
            max-width: 120px;
        }

        button {
            width: 100%;
        }
    }

    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0.5rem;
        color: #e0e0e0;
    }
</style>
