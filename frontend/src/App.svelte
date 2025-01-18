<script>
  import { onMount } from 'svelte';
  import { loading, error } from './lib/stores/store';
  import { auth } from './lib/stores/authStore.svelte';
  import { actions } from './lib/stores/store';
  import { get } from './lib/api/client';
  
  // Components
  import Auth from './components/Auth.svelte';
  
  // Views
  import Home from './views/Home.svelte';
  import Grievances from './views/Grievances.svelte';
  import Stakeholders from './views/Stakeholders.svelte';
  import Admin from './views/Admin.svelte';
  
  let currentRoute = $state('home');
  
  function handleNavigation(route) {
    currentRoute = route;
    actions.clearError();
  }
  
  async function loadInitialData() {
    if (!auth.isAuthenticated) return;
    
    try {
        actions.setLoading(true);
        const [grievancesData, userData] = await Promise.all([
            get('/grievances'),
            get('/users/me')
        ]);
        actions.setGrievances(grievancesData);
        auth.setUser(userData);
    } catch (e) {
        actions.setError(e.message);
        console.error('Failed to load initial data:', e);
    } finally {
        actions.setLoading(false);
    }
  }

  onMount(() => {
    auth.initialize();
  });

  $effect(() => {
    if (auth.isAuthenticated) {
      loadInitialData();
    }
  });
</script>

<main>
  <nav>
    <div class="nav-content">
      <ul class="nav-links">
        <li>
          <button 
            class:active={currentRoute === 'home'} 
            onclick={() => handleNavigation('home')}
          >
            Home
          </button>
        </li>
        {#if auth.isAuthenticated}
          <li>
            <button 
              class:active={currentRoute === 'grievances'} 
              onclick={() => handleNavigation('grievances')}
            >
              Grievances
            </button>
          </li>
          {#if auth.isSupervisor}
            <li>
              <button 
                class:active={currentRoute === 'stakeholders'} 
                onclick={() => handleNavigation('stakeholders')}
              >
                Stakeholders
              </button>
            </li>
            <li>
              <button 
                class:active={currentRoute === 'admin'} 
                onclick={() => handleNavigation('admin')}
              >
                Manage
              </button>
            </li>
          {/if}
        {/if}
      </ul>
      <div class="auth-container">
        <Auth />
      </div>
    </div>
  </nav>

  {#if $loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
  {/if}

  {#if $error}
    <div class="error">
      <p>{$error}</p>
      <button onclick={actions.clearError}>Dismiss</button>
    </div>
  {/if}

  <div class="content">
    {#if !auth.isAuthenticated}
      <div class="message">
        Please log in to access the application.
      </div>
    {:else if currentRoute === 'home'}
      <Home />
    {:else if currentRoute === 'grievances'}
      <Grievances />
    {:else if currentRoute === 'stakeholders'}
      <Stakeholders />
    {:else if currentRoute === 'admin'}
      <Admin />
    {/if}
  </div>
</main>

<style>
  :global(body) {
    background-color: #1a1a1a;
    color: #e0e0e0;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
  }

  :global(button) {
    font-family: inherit;
  }

  main {
    width: min(1200px, 100% - 40px);
    margin: 0 auto;
    padding: 20px 0;
  }

  nav {
    background: #2d2d2d;
    padding: 0.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .nav-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
  }

  .nav-links {
    display: flex;
    gap: 0.5rem;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .auth-container {
    margin-left: auto;
  }

  button {
    background: transparent;
    border: none;
    color: #e0e0e0;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  button:hover {
    background: #3d3d3d;
  }

  button.active {
    background: #64b5f6;
    color: #1a1a1a;
  }

  @media (max-width: 768px) {
    .nav-content {
      flex-direction: column;
      gap: 1rem;
    }

    .nav-links {
      flex-wrap: wrap;
      justify-content: center;
    }

    .auth-container {
      width: 100%;
    }
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #e0e0e0;
  }

  .spinner {
    width: 40px;
    height: 40px;
    margin: 0 auto 1rem;
    border: 4px solid #2d2d2d;
    border-top: 4px solid #64b5f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .error {
    background: #3d2626;
    border: 1px solid #ff5252;
    color: #ff5252;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .error button {
    background: #ff5252;
    color: #1a1a1a;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .error button:hover {
    background: #ff7070;
  }

  .content {
    background: #2d2d2d;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    width: 100%;
    box-sizing: border-box;
  }

  :global(.card) {
    background: #3d3d3d;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  :global(input), :global(textarea), :global(select) {
    background: #3d3d3d;
    border: 1px solid #4d4d4d;
    color: #e0e0e0;
    padding: 0.5rem;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
  }

  :global(input:focus), :global(textarea:focus), :global(select:focus) {
    outline: none;
    border-color: #64b5f6;
    box-shadow: 0 0 0 2px rgba(100, 181, 246, 0.2);
  }

  :global(button) {
    background: #64b5f6;
    color: #1a1a1a;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  :global(button:hover) {
    background: #90caf9;
  }

  :global(button.delete-btn) {
    background: #ff5252;
  }

  :global(button.delete-btn:hover) {
    background: #ff7070;
  }

  :global(h1), :global(h2), :global(h3), :global(h4) {
    color: #e0e0e0;
    margin-top: 0;
  }

  :global(.stat-card) {
    background: #3d3d3d;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  :global(.stat-number) {
    color: #64b5f6;
  }

  @media (max-width: 768px) {
    main {
      width: 100%;
      padding: 10px;
    }

    .content {
      padding: 1rem;
    }
  }

  .message {
    text-align: center;
    padding: 2rem;
    color: #e0e0e0;
  }
</style>
