<script>
  import { onMount } from 'svelte';
  import {store } from './lib/stores/store.svelte';
  import { auth } from './lib/stores/authStore.svelte';
  import { get } from './lib/api/client';
  import { Shield, User, Target } from 'lucide-svelte';
  
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
        const [stakeholdersData, grievancesData, userData] = await Promise.all([
            get('/stakeholders'),
            get('/grievances'),
            get('/users/me')
        ]);
        store.setStakeholders(stakeholdersData);
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
      <div class="welcome-container">
        <div class="welcome-content">
          <h1>Welcome to the Informal Grievance Module</h1>
          <h2>Resolve issues at the lowest level.</h2>
          
          <div class="features">
            <div class="feature-card">
              <Shield size={24} />
              <h3>Secure Grievance Management</h3>
              <p>A secure platform for personnel to submit and track grievances with confidentiality.</p>
            </div>
            
            <div class="feature-card">
              <User size={24} />
              <h3>Role-Based Access</h3>
              <p>Dedicated interfaces for users, supervisors, and administrators to ensure proper handling of cases.</p>
            </div>
            
            <div class="feature-card">
              <Target size={24} />
              <h3>Real-Time Updates</h3>
              <p>Track the status of your grievances in real-time with a transparent resolution process.</p>
            </div>
          </div>

          <div class="auth-prompt">
            <p>Please log in to access the application. New users should register using their JSIS credentials.</p>
          </div>
        </div>
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

  .welcome-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 200px);
    padding: 2rem;
  }

  .welcome-content {
    max-width: 900px;
    text-align: center;
  }

  .welcome-content h1 {
    font-size: 2.5rem;
    font-weight: 600;
    margin: 0;
    color: var(--primary-red, #C41E3A);
  }

  .welcome-content h2 {
    font-size: 1.2rem;
    font-weight: 400;
    margin: 0.5rem 0 2rem;
    color: var(--text-light, #e0e0e0);
    opacity: 0.8;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin: 3rem 0;
  }

  .feature-card {
    background: var(--gray-dark, #333333);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
  }

  .feature-card:hover {
    transform: translateY(-5px);
  }

  .feature-card :global(svg) {
    color: var(--primary-red, #C41E3A);
    margin-bottom: 1rem;
  }

  .feature-card h3 {
    font-size: 1.1rem;
    font-weight: 500;
    margin: 0 0 1rem;
    color: var(--text-light, #e0e0e0);
  }

  .feature-card p {
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0;
    color: var(--text-light, #e0e0e0);
    opacity: 0.8;
  }

  .auth-prompt {
    margin-top: 3rem;
    padding: 1.5rem;
    background: var(--primary-dark, #1A1A1A);
    border-radius: 8px;
    border: 1px solid var(--gray-medium, #666666);
  }

  .auth-prompt p {
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
    color: var(--text-light, #e0e0e0);
  }

  @media (max-width: 768px) {
    .features {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .welcome-content h1 {
      font-size: 2rem;
    }

    .welcome-content h2 {
      font-size: 1rem;
    }

    .feature-card {
      padding: 1.5rem;
    }
  }
</style>
