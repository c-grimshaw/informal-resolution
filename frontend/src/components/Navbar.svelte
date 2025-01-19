<script>
    import { auth } from '../lib/stores/authStore.svelte';
    import { store } from '../lib/stores/store.svelte';
    import { 
        Home as HomeIcon, 
        FileText, 
        Users, 
        Settings,
        HelpCircle 
    } from 'lucide-svelte';
    import Auth from './Auth.svelte';

    let {currentRoute = $bindable()} = $props();

    function handleNavigation(route) {
        currentRoute = route;
        store.clearError();
    }
</script>

<nav>
    <div class="nav-content">
        <ul class="nav-links">
            <li>
                <button 
                    class:active={currentRoute === 'home'} 
                    onclick={() => handleNavigation('home')}
                >
                    <HomeIcon size={16} />
                    <span>Home</span>
                </button>
            </li>
            {#if auth.isAuthenticated}
                <li>
                    <button 
                        class:active={currentRoute === 'grievances'} 
                        onclick={() => handleNavigation('grievances')}
                    >
                        <FileText size={16} />
                        <span>Grievances</span>
                    </button>
                </li>
                {#if auth.isAdmin}
                    <li>
                        <button 
                            class:active={currentRoute === 'stakeholders'} 
                            onclick={() => handleNavigation('stakeholders')}
                        >
                            <Users size={16} />
                            <span>Stakeholders</span>
                        </button>
                    </li>
                    <li>
                        <button 
                            class:active={currentRoute === 'admin'} 
                            onclick={() => handleNavigation('admin')}
                        >
                            <Settings size={16} />
                            <span>Manage</span>
                        </button>
                    </li>
                {/if}
                <li>
                    <button 
                        class:active={currentRoute === 'help'} 
                        onclick={() => handleNavigation('help')}
                    >
                        <HelpCircle size={16} />
                        <span>Help</span>
                    </button>
                </li>
            {/if}
        </ul>
        <div class="auth-container">
            <Auth />
        </div>
    </div>
</nav>

<style>
    nav {
        background: #2d2d2d;
        padding: 0.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        position: sticky;
        top: 0;
        z-index: 100;
        border-radius: 8px;
    }

    .nav-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .nav-links {
        display: flex;
        gap: 0.5rem;
        list-style: none;
        margin: 0;
        padding: 0;
        flex-wrap: wrap;
    }

    .nav-links button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        font-weight: 500;
        white-space: nowrap;
        transition: all 0.2s ease;
        background: transparent;
        border: none;
        color: #e0e0e0;
        border-radius: 4px;
        min-height: 36px;
        position: relative;
        overflow: hidden;
    }

    .nav-links button::before {
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

    .nav-links button:hover {
        color: #C8102E;
    }

    .nav-links button:hover::before {
        transform: translateX(0);
    }

    .nav-links button.active {
        background: #C8102E;
        color: white;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(200, 16, 46, 0.2);
    }

    .nav-links button.active:hover {
        background: #E31837;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(200, 16, 46, 0.3);
    }

    .nav-links :global(svg) {
        width: 16px;
        height: 16px;
        flex-shrink: 0;
        transition: all 0.2s ease;
    }

    .nav-links button:hover :global(svg) {
        transform: scale(1.1) rotate(5deg);
        color: #C8102E;
    }

    .nav-links button.active:hover :global(svg) {
        color: white;
        transform: scale(1.1) rotate(-5deg);
    }

    .auth-container {
        flex: 1;
        min-width: 200px;
        display: flex;
        justify-content: flex-end;
    }

    @media (max-width: 1024px) {
        .nav-content {
            gap: 0.75rem;
        }
    }

    @media (max-width: 768px) {
        nav {
            padding: 0.75rem;
            border-radius: 6px;
        }

        .nav-content {
            flex-direction: column;
            align-items: stretch;
        }

        .nav-links {
            justify-content: flex-start;
            width: 100%;
        }

        .auth-container {
            width: 100%;
            justify-content: stretch;
            padding-top: 0.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    }

    @media (max-width: 480px) {
        nav {
            padding: 0.5rem;
            border-radius: 0;
            margin: -0.25rem;
            width: calc(100% + 0.5rem);
        }

        .nav-links {
            flex-direction: column;
        }

        .nav-links button {
            width: 100%;
            justify-content: flex-start;
            padding: 0.75rem;
        }
    }

    @media (max-width: 360px) {
        nav {
            margin: 0;
            width: 100%;
        }
    }
</style> 