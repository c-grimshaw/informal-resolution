<script>
  import { onMount } from 'svelte';
  import {store } from './lib/stores/store.svelte';
  import { auth } from './lib/stores/authStore.svelte';
  import { get } from './lib/api/client';
  
  // Components
  import Navbar from './components/Navbar.svelte';
  
  // Views
  import Home from './views/Home.svelte';
  import Grievances from './views/Grievances.svelte';
  import Stakeholders from './views/Stakeholders.svelte';
  import Admin from './views/Admin.svelte';
  import Help from './views/Help.svelte';
  
  let currentRoute = $state('home');
  
  async function loadInitialData() {
    if (!auth.isAuthenticated) return;
    
    try {
        store.setLoading(true);
        const [grievancesData, userData] = await Promise.all([
            get('/grievances'),
            get('/users/me')
        ]);
        store.setGrievances(grievancesData);
        auth.setUser(userData);
    } catch (e) {
        store.setError(e.message);
        console.error('Failed to load initial data:', e);
    } finally {
        store.setLoading(false);
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

  $effect(() => {
    // Keep currentRoute in sync with auth store
    if (auth.currentRoute) {
      currentRoute = auth.currentRoute;
    }
  });
</script>

<main>
  <Navbar bind:currentRoute />

  {#if store.loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
  {/if}

  {#if store.error}
    <div class="error">
      <p>{store.error}</p>
      <button onclick={store.clearError}>Dismiss</button>
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
    {:else if currentRoute === 'help'}
      <Help />
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
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  :global(*) {
    box-sizing: border-box;
  }

  main {
    width: min(1200px, 95%);
    margin: 0 auto;
    padding: 0.5rem;
  }

  .content {
    background: #2d2d2d;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    width: 100%;
  }

  .error {
    background: #3d2626;
    border: 1px solid #ff5252;
    color: #ff5252;
    padding: 0.75rem;
    margin: 0.75rem 0;
    border-radius: 4px;
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }

  .error p {
    margin: 0;
    flex: 1;
    min-width: 200px;
  }

  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 2rem 1rem;
  }

  .loading p {
    margin: 0;
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #2d2d2d;
    border-top: 3px solid #C8102E;
    border-radius: 50%;
    animation: spin 1s linear infinite;
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
    padding: 0.75rem;
    border-radius: 4px;
    width: 100%;
    font-size: 0.95rem;
  }

  :global(button) {
    background: #C8102E;
    color: white;
    border: none;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.95rem;
    font-weight: 500;
  }

  :global(button:hover) {
    background: #E31837;
    transform: translateY(-1px);
  }

  :global(button:disabled) {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }

  /* Tablet and smaller desktop */
  @media (max-width: 1024px) {
    main {
      width: min(1024px, 95%);
    }
  }

  /* Tablet */
  @media (max-width: 768px) {
    main {
      width: 95%;
      padding: 0.5rem;
    }

    .content {
      padding: 1rem;
    }
  }

  /* Mobile */
  @media (max-width: 480px) {
    main {
      width: 100%;
      padding: 0.25rem;
    }

    .content {
      padding: 0.75rem;
      border-radius: 6px;
    }

    :global(.card) {
      padding: 0.75rem;
      margin-bottom: 0.75rem;
    }

    .error {
      flex-direction: column;
      align-items: stretch;
      gap: 0.5rem;
    }

    .error p {
      min-width: unset;
    }
  }

  /* Small Mobile */
  @media (max-width: 360px) {
    main {
      padding: 0;
    }

    .content {
      border-radius: 0;
    }

    :global(input), :global(textarea), :global(select) {
      font-size: 16px; /* Prevents zoom on iOS */
    }
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
