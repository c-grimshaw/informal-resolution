<script>
  import { store } from '../lib/stores/store.svelte';
  import KanbanBoard from '../components/KanbanBoard.svelte';
  import GrievanceTable from '../components/GrievanceTable.svelte';
  import ViewToggle from '../components/ViewToggle.svelte';
  import Chart from 'chart.js/auto';

  let view = $state('table');
  let statusChartCanvas;
  let trendsChartCanvas;
  let charts = [];

  function createCharts() {
    // Clear any existing charts
    charts.forEach(chart => chart.destroy());
    charts = [];

    // Status Distribution Chart
    const statusData = {
      pending: store.grievances.filter(g => g.status === 'pending').length,
      in_progress: store.grievances.filter(g => g.status === 'in_progress').length,
      resolved: store.grievances.filter(g => g.status === 'resolved').length
    };

    const statusChart = new Chart(statusChartCanvas, {
      type: 'doughnut',
      data: {
        labels: ['Pending', 'In Progress', 'Resolved'],
        datasets: [{
          data: [statusData.pending, statusData.in_progress, statusData.resolved],
          backgroundColor: ['#FFA500', '#64B5F6', '#4CAF50']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#e0e0e0',
              padding: 20
            }
          }
        }
      }
    });
    charts.push(statusChart);

    // Monthly Trends Chart
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const monthlyData = {};
    
    // Process grievances to get date range
    store.grievances.forEach(g => {
      const date = new Date(g.created_at);
      const key = `${date.getFullYear()}-${date.getMonth()}`;
      monthlyData[key] = (monthlyData[key] || 0) + 1;
    });

    // Sort the keys to get chronological order
    const sortedKeys = Object.keys(monthlyData).sort();
    
    // Take the last 6 months of data (or all if less than 6)
    const recentKeys = sortedKeys.slice(-6);
    
    // Create labels and data arrays
    const labels = recentKeys.map(key => {
      const [year, month] = key.split('-');
      return `${months[parseInt(month)]} ${year}`;
    });
    
    const data = recentKeys.map(key => monthlyData[key]);

    const trendsChart = new Chart(trendsChartCanvas, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Grievances',
          data,
          borderColor: '#64B5F6',
          tension: 0.4,
          fill: true,
          backgroundColor: 'rgba(100, 181, 246, 0.1)'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 5,
            right: 5,
            top: 5,
            bottom: 5
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1,
              color: '#e0e0e0',
              padding: 5,
              font: {
                size: 10
              }
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          },
          x: {
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
              color: '#e0e0e0',
              padding: 5,
              maxRotation: 45,
              font: {
                size: 10
              }
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              title: (context) => context[0].label,
              label: (context) => `${context.parsed.y} grievance${context.parsed.y !== 1 ? 's' : ''}`
            }
          }
        }
      }
    });
    charts.push(trendsChart);
  }

  $effect(() => {
    if (store.grievances && statusChartCanvas && trendsChartCanvas) {
      createCharts();
    }
  });

  function handleViewToggle(event) {
    view = event.detail;
  }
</script>

<div class="admin-container">
  <div class="header">
    <h1>Grievance Management</h1>
  </div>

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

  <div class="charts-grid">
    <div class="chart-card">
      <h3>Status Distribution</h3>
      <div class="chart-container">
        <canvas bind:this={statusChartCanvas}></canvas>
      </div>
    </div>
    <div class="chart-card">
      <h3>Monthly Trends</h3>
      <div class="chart-container">
        <canvas bind:this={trendsChartCanvas}></canvas>
      </div>
    </div>
  </div>

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
    color: var(--text-light, #FFFFFF);
    font-weight: 300;
    font-size: 2rem;
    margin: 0;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
    width: 100%;
  }

  .stat-card {
    background: var(--gray-dark, #333333);
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .stat-card h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-light, #FFFFFF);
    opacity: 0.8;
  }

  .stat-number {
    font-size: 2rem;
    font-weight: 300;
    margin: 0;
    color: var(--text-light, #FFFFFF);
  }

  .charts-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin-bottom: 2rem;
    width: 100%;
    max-width: 100%;
    overflow: hidden;
  }

  .chart-card {
    background: var(--gray-dark, #333333);
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    width: 100%;
    height: 300px;
    display: flex;
    flex-direction: column;
  }

  .chart-card h3 {
    margin: 0 0 0.5rem 0;
    text-align: center;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-light, #FFFFFF);
    opacity: 0.8;
    flex-shrink: 0;
  }

  .chart-container {
    position: relative;
    flex: 1;
    min-height: 0;
    width: 100%;
    height: calc(100% - 1.5rem);
  }

  canvas {
    max-width: 100%;
    height: 100% !important;
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
    color: var(--text-light, #FFFFFF);
    font-weight: 300;
    font-size: 1.5rem;
    margin: 0;
  }

  .content {
    width: 100%;
  }

  @media (max-width: 1200px) {
    .charts-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .chart-card {
      height: 250px;
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

    .charts-grid {
      gap: 1rem;
    }

    .chart-card {
      height: 300px;
    }

    .view-header {
      flex-direction: column;
      gap: 10px;
      padding: 0;
    }
  }
</style> 