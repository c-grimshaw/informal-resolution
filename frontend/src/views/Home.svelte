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
  <h1>Informal Resolution System</h1>
  
  <div class="grievances-section">
    <h2>My Grievances</h2>
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

  .grievances-section {
    margin-top: 3rem;
  }
</style> 