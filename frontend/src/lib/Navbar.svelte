<script>
    import { auth } from "$lib/stores/authStore.svelte";
    import { store } from "$lib/stores/store.svelte";
    import {
        Home as HomeIcon,
        FileText,
        Users,
        Settings,
        HelpCircle,
    } from "lucide-svelte";
    import Auth from "./Auth.svelte";
</script>

<nav>
    <div class="nav-content">
        <ul class="nav-links">
            {#snippet navlink(href, Icon, label)}
                <li>
                    <a href={href}>
                        <button>
                            <Icon size={16} />
                            <span>{label}</span>
                        </button>
                    </a>
                </li>
            {/snippet}

            {@render navlink("/home", HomeIcon, "Home")}

            {#if auth.isAuthenticated}
                {@render navlink("/grievance", FileText, "Grievances")}
                {#if auth.isAdmin || auth.isSupervisor}
                    {@render navlink("/manage", Settings, "Manage")}
                {/if}

                {#if auth.isAdmin}
                    {@render navlink("/stakeholders", Users, "Stakeholders")}
                {/if}

                {@render navlink("/help", HelpCircle, "Help")}
            {/if}
        </ul>

        <div class="auth-container">
            <Auth />
        </div>
    </div>
</nav>

<style>
    /* Base styles */
nav {
    background: #2d2d2d;
    padding: .75rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px #0005;
    position: sticky;
    top: 0;
    z-index: 100;
    border-radius: 8px;
}

/* Layout containers */
.nav-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.nav-links {
    display: flex;
    gap: .5rem;
    list-style: none;
    margin: 0;
    padding: 0;
    flex-wrap: wrap;
}

.auth-container {
    flex: 1;
    min-width: 200px;
    display: flex;
    justify-content: flex-end;
}

/* Button styles */
.nav-links button {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    padding: .5rem .75rem;
    font-size: .9rem;
    font-weight: 500;
    white-space: nowrap;
    background: transparent;
    border: none;
    color: #e0e0e0;
    border-radius: 4px;
    min-height: 36px;
    position: relative;
    overflow: hidden;
}

.nav-links button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: #c8102e1a;
    transform: translateX(-100%);
    transition: .3s ease;
}

.nav-links button:hover {
    color: #c8102e;
}

.nav-links button:hover::before {
    transform: translateX(0);
}

.nav-links :global(svg) {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
    transition: .2s ease;
}

.nav-links button:hover :global(svg) {
    transform: scale(1.1) rotate(5deg);
    color: #c8102e;
}

/* Media queries */
@media (max-width: 1024px) {
    .nav-content { gap: .75rem; }
}

@media (max-width: 768px) {
    nav {
        padding: .75rem;
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
        padding-top: .5rem;
        border-top: 1px solid #fff1;
    }
}

@media (max-width: 480px) {
    nav {
        padding: .5rem;
        border-radius: 0;
        margin: -.25rem;
        width: calc(100% + .5rem);
    }
    .nav-links {
        flex-direction: column;
    }
    .nav-links button {
        width: 100%;
        justify-content: flex-start;
        padding: .75rem;
    }
}

@media (max-width: 360px) {
    nav {
        margin: 0;
        width: 100%;
    }
}
</style>
