<script>
  import { store } from "$lib/stores/store.svelte";
  import { auth } from "$lib/stores/authStore.svelte";
  import KanbanBoard from "$lib/kanban/KanbanBoard.svelte";
  import GrievanceTable from "$lib/GrievanceTable.svelte";
  import ViewToggle from "$lib/ViewToggle.svelte";
  import StatusChart from "$lib/charts/StatusChart.svelte";
  import TrendsChart from "$lib/charts/TrendsChart.svelte";
  import UnitDistributionChart from "$lib/charts/UnitDistributionChart.svelte";
  import { ChevronDown } from "lucide-svelte";
  import { slide } from "svelte/transition";

  let view = $state("table");
  let isChartsVisible = $state(false);

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
        <h3>Total Grievances This Month</h3>
        {#if store.grievances.length > 0}
          {@const now = new Date()}
          {@const thisMonth = store.grievances.filter((g) => {
            const date = new Date(g.created_at);
            return (
              date.getMonth() === now.getMonth() &&
              date.getFullYear() === now.getFullYear()
            );
          })}
          {@const lastMonth = store.grievances.filter((g) => {
            const date = new Date(g.created_at);
            const lastMonthDate = new Date(
              now.getFullYear(),
              now.getMonth() - 1,
            );
            return (
              date.getMonth() === lastMonthDate.getMonth() &&
              date.getFullYear() === lastMonthDate.getFullYear()
            );
          })}
          {@const percentChange = lastMonth.length
            ? ((thisMonth.length - lastMonth.length) / lastMonth.length) * 100
            : 0}
          <p class="stat-number">{thisMonth.length}</p>
          {#if lastMonth.length > 0}
            <p
              class="stat-change"
              class:increase={percentChange > 0}
              class:decrease={percentChange < 0}
            >
              {percentChange > 0 ? "↑" : "↓"}
              {Math.abs(percentChange).toFixed(1)}% from last month
            </p>
          {/if}
        {/if}
      </div>
      <div class="stat-card">
        <h3>Resolved</h3>
        <p class="stat-number">
          {store.grievances.filter((g) => g.status === "resolved").length}
        </p>
      </div>
      <div class="stat-card">
        <h3>Pending</h3>
        <p class="stat-number">
          {store.grievances.filter((g) => g.status === "pending").length}
        </p>
      </div>
    </div>

    <div class="charts-section">
      <button
        class="charts-toggle"
        onclick={() => (isChartsVisible = !isChartsVisible)}
      >
        <span>Analytics Dashboard</span>
        <div
          style:transform={isChartsVisible ? "rotateX(0)" : "rotateX(180deg)"}
        >
          <ChevronDown size={20} />
        </div>
      </button>

      {#if isChartsVisible}
        <div
          class="charts-grid"
          transition:slide
          class:two-charts={!auth.isAdmin}
        >
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
      {#if view === "kanban"}
        <KanbanBoard />
      {:else}
        <GrievanceTable
          grievances={store.grievances}
          showColumns={[
            "submitter_name",
            "rank",
            "unit",
            "position",
            "grievance_type",
            "status",
            "created_at",
          ]}
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
    color: var(--text-light, #ffffff);
    margin: 0 0 1.5rem 0;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
    width: 100%;
  }

  .stat-card {
    background: var(--primary-dark, #1a1a1a);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 4px;
    padding: 0.75rem;
  }

  .stat-card h3 {
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0;
    color: var(--text-light, #ffffff);
    opacity: 0.9;
  }

  .stat-number {
    font-size: 1.5rem;
    font-weight: 500;
    margin: 0.5rem 0 0 0;
    color: var(--text-light, #ffffff);
  }

  .stat-change {
    font-size: 0.8em;
    margin-top: 0.25rem;
    opacity: 0.9;
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
    background: var(--primary-dark, #1a1a1a);
    border: none;
    border-radius: 8px;
    color: var(--text-light, #ffffff);
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
    color: var(--text-light, #ffffff);
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

    .charts-grid,
    .charts-grid.two-charts {
      grid-template-columns: 1fr;
    }

    .view-header {
      flex-direction: column;
      gap: 10px;
      padding: 0;
    }
  }

  .stat-change {
    font-size: 0.9em;
    margin-top: 0.5rem;
  }

  .stat-change.increase {
    color: #ff4444;
  }

  .stat-change.decrease {
    color: #4caf50;
  }
</style>
