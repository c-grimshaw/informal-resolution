<script>
  import { store } from '../lib/stores/store.svelte';
  import { auth } from '../lib/stores/authStore.svelte';
  import { get } from '../lib/api/client';
  import GrievanceTable from '../components/GrievanceTable.svelte';

  let userGrievances = $state([]);

  async function loadUserGrievances() {
    try {
      const data = await get(`/grievances/user/${auth.user.id}`);
      userGrievances = data;
    } catch (error) {
      console.error('Failed to load user grievances:', error);
    }
  }

  $effect(() => {
    if (auth.user?.id) {
      loadUserGrievances();
    }
  });

  function handleGrievanceDelete(grievanceId) {
    userGrievances = userGrievances.filter(g => g.id !== grievanceId);
  }
</script>

<div class="home">
  <h1>Welcome to the Grievance Management System</h1>
  
  <div class="stats">
    <div class="stat-card">
      <h3>Your Active Grievances</h3>
      <p class="stat-number">{userGrievances.length}</p>
    </div>
    
    {#if auth.isSupervisor}
      <div class="stat-card">
        <h3>Total Stakeholders</h3>
        <p class="stat-number">{store.stakeholders.length}</p>
      </div>
    {/if}
  </div>

  <div class="grievances-section">
    <h2>Your Grievances</h2>
    <GrievanceTable 
      grievances={userGrievances}
      showColumns={['grievance_type', 'status', 'created_at']}
      canEditStatus={false}
      readonly={true}
      canDelete={true}
      onDelete={handleGrievanceDelete}
      showFilters={false}
    />
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

  .stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 2rem;
  }

  .stat-card {
    background: var(--gray-dark, #333333);
    padding: 1.5rem;
    border-radius: 8px;
    min-width: 200px;
    border: 1px solid var(--gray-medium, #666666);
  }

  .stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary-red, #C41E3A);
  }

  .grievances-section {
    margin-top: 3rem;
  }

  @media (max-width: 768px) {
    .stats {
      flex-direction: column;
      align-items: center;
    }

    .stat-card {
      width: 100%;
    }
  }
</style> 