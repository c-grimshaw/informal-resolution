<script>
  import { onMount } from 'svelte';
  import { get } from '../lib/api/client';
  import { store } from '../lib/stores/store.svelte';
  import { auth } from '../lib/stores/authStore.svelte';
  import StakeholdersTable from '../components/StakeholdersTable.svelte';

  let stakeholders = $state([]);

  onMount(() => {
    fetchStakeholders();
    // Listen for profile updates
    window.addEventListener('profileUpdate', fetchStakeholders);
    // Return cleanup function
    return () => {
      window.removeEventListener('profileUpdate', fetchStakeholders);
    };
  });

  async function fetchStakeholders() {
    try {
      store.setLoading(true);
      const response = await get('/users/all');
      console.log(response);
      stakeholders = response;
    } catch (error) {
      store.setError('Failed to fetch stakeholders');
    } finally {
      store.setLoading(false);
    }
  }

  function handleDelete(userId) {
    stakeholders = stakeholders.filter(s => s.id !== userId);
  }
</script>

<div class="stakeholders-view">
  <header>
    <h1>Stakeholders</h1>
  </header>

  <StakeholdersTable 
    stakeholders={stakeholders}
    canDelete={auth.isAdmin}
    onDelete={handleDelete}
  />
</div>

<style>
  .stakeholders-view {
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  header {
    margin-bottom: 1.5rem;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
    margin: 0;
  }
</style> 