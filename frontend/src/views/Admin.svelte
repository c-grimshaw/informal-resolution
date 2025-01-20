<script>
  import { store } from '../lib/stores/store.svelte';
  import { auth } from '../lib/stores/authStore.svelte';
  import { get } from '../lib/api/client';
  import KanbanBoard from '../components/KanbanBoard.svelte';
  import GrievanceTable from '../components/GrievanceTable.svelte';
  import ViewToggle from '../components/ViewToggle.svelte';
  import StatusChart from '../components/StatusChart.svelte';
  import TrendsChart from '../components/TrendsChart.svelte';
  import UnitDistributionChart from '../components/UnitDistributionChart.svelte';
  import { ChevronDown } from 'lucide-svelte';
  import { slide } from 'svelte/transition';
  import { onMount } from 'svelte';

  let view = $state('table');
  let isChartsVisible = $state(false);

  async function loadGrievances() {
    try {
      const data = await get('/grievances');
      store.setGrievances(data);
    } catch (error) {
      store.setError('Failed to load grievances: ' + error.message);
    }
  }

  onMount(() => {
    loadGrievances();
  });

  function handleViewToggle(event) {
    view = event.detail;
  }
</script>

<div class="admin-container">
  <div class="header">
    <h1>Grievance Management</h1>
  </div>

  {#if auth.isSupervisor || auth.isAdmin}
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total Grievances</h3>
        <p class="stat-number">{store.grievances.length}</p>
      </div>
      <div class="stat-card">
        <h3>Resolved</h3>
        <p class="stat-number">
          {store.grievances.filter(g => g.status === 'resolved').length}
        </p>
      </div>
      <div class="stat-card">
        <h3>Pending</h3>
        <p class="stat-number">
          {store.grievances.filter(g => g.status === 'pending').length}
        </p>
      </div>
      <div class="stat-card">
        <h3>Stakeholders</h3>
        <p class="stat-number">{store.stakeholders.length}</p>
      </div>
    </div>

    <div class="charts-section">
      <button class="charts-toggle" onclick={() => isChartsVisible = !isChartsVisible}>
        <span>Analytics Dashboard</span>
        <div style:transform={isChartsVisible ? 'rotateX(0)' : 'rotateX(180deg)'}>
          <ChevronDown size={20} />
        </div>
      </button>
      
      {#if isChartsVisible}
        <div class="charts-grid" transition:slide class:two-charts={!auth.isAdmin}>
          <StatusChart grievances={store.grievances} />
          <TrendsChart grievances={store.grievances} />
          {#if auth.isAdmin}
            <UnitDistributionChart grievances={store.grievances} />
          {/if}
        </div>
      {/if}
    </div>
  {/if}

  <div class="view-section">
    <div class="view-header">
      <h2>Grievance Management Board</h2>
        <ViewToggle {view} on:toggle={handleViewToggle} />
    </div>
    <div class="content">
      {#if view === 'kanban'}
        <KanbanBoard grievances={store.grievances} />
      {:else}
        <GrievanceTable 
          grievances={store.grievances}
          showColumns={['submitter_name', 'rank', 'unit', 'position', 'grievance_type', 'status', 'created_at']}
          canEditStatus={true}
          readonly={false}
        />
      {/if}
    </div>
  </div>
</div>

<style>
  .admin-container {
    width: 100%;
    margin: 0;
    padding: 0;
    min-height: calc(100vh - 250px);
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
    margin: 0 0 1.5rem 0;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
    width: 100%;
  }

  .stat-card {
    background: var(--primary-dark, #1A1A1A);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .stat-card h3 {
    font-size: 0.9rem;
    font-weight: 400;
    color: var(--text-light, #FFFFFF);
    margin: 0 0 1rem 0;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .stat-number {
    font-size: 2rem;
    font-weight: 600;
    color: var(--primary-red, #C41E3A);
    margin: 0;
  }

  .charts-section {
    margin: 2rem 0;
  }

  .charts-toggle {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: var(--primary-dark, #1A1A1A);
    border: none;
    border-radius: 8px;
    color: var(--text-light, #FFFFFF);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .charts-toggle:hover {
    background: var(--gray-dark, #333333);
  }

  .charts-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1rem;
  }

  .charts-grid.two-charts {
    grid-template-columns: repeat(2, 1fr);
  }

  .view-section {
    margin-top: 2rem;
    width: 100%;
  }

  .view-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .view-header h2 {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
    margin: 0;
  }

  .content {
    width: 100%;
  }

  @media (max-width: 1200px) {
    .charts-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .charts-grid.two-charts {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 768px) {
    .admin-container {
      padding: 0;
      min-height: calc(100vh - 200px);
    }

    .header {
      flex-direction: column;
      gap: 10px;
      align-items: flex-start;
    }

    h1 {
      font-size: 1.5rem;
    }

    .stats-grid {
      gap: 0.75rem;
    }

    .charts-grid, .charts-grid.two-charts {
      grid-template-columns: 1fr;
    }

    .view-header {
      flex-direction: column;
      gap: 10px;
      padding: 0;
    }
  }
</style> 