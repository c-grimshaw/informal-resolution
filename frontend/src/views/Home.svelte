<script>
  import { store } from '../lib/stores/store.svelte';
  import { auth } from '../lib/stores/authStore.svelte';
  import { get } from '../lib/api/client';
  import GrievanceTable from '../components/GrievanceTable.svelte';

  async function loadUserGrievances() {
    try {
      const data = await get(`/grievances/user/${auth.user.id}`);
      store.setGrievances(data);
    } catch (error) {
      console.error('Failed to load user grievances:', error);
      store.setError('Failed to load grievances');
    }
  }

  $effect(() => {
    if (auth.user?.id) {
      loadUserGrievances();
    }
  });

  function handleGrievanceDelete(grievanceId) {
    store.deleteGrievance(grievanceId);
  }
</script>

<div class="home">
  <h1>Informal Resolution System</h1>
  
  <div class="grievances-section">
    <h2>My Grievances</h2>
    {#if store.grievances.length === 0}
      <div class="empty-state">
        <p>You have no current grievances in the system.</p>
        <p>To submit a new grievance, click the "Grievances" button in the navigation bar.</p>
      </div>
    {:else}
      <GrievanceTable 
        grievances={store.grievances}
        showColumns={['grievance_type', 'status', 'created_at']}
        canEditStatus={false}
        readonly={true}
        canDelete={true}
        onDelete={handleGrievanceDelete}
        showFilters={false}
      />
    {/if}
  </div>
</div>

<style>
  .home {
    text-align: center;
  }

  h1 {
    margin-bottom: 2rem;
    color: var(--text-light, #FFFFFF);
  }

  h2 {
    margin: 2rem 0;
    color: var(--text-light, #FFFFFF);
    text-align: left;
  }

  .grievances-section {
    margin-top: 3rem;
  }

  .empty-state {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    color: var(--text-light, #FFFFFF);
  }

  .empty-state p {
    margin: 0.5rem 0;
    line-height: 1.5;
  }

  .empty-state p:first-child {
    font-size: 1.1em;
    font-weight: 500;
  }

  .empty-state p:last-child {
    color: var(--gray-light, #999999);
  }
</style> 