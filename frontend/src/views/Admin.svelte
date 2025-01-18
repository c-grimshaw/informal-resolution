<script>
  import { onMount } from 'svelte';
  import { grievances, stakeholders } from '../lib/stores/store';
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
      pending: $grievances.filter(g => g.status === 'pending').length,
      in_progress: $grievances.filter(g => g.status === 'in_progress').length,
      resolved: $grievances.filter(g => g.status === 'resolved').length
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
    const monthlyData = Array(6).fill(0);
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    
    // Get the last 6 months in chronological order
    const labels = [];
    for (let i = 5; i >= 0; i--) {
      const monthIndex = (currentMonth - i + 12) % 12;
      labels.unshift(months[monthIndex]);
    }

    $grievances.forEach(g => {
      const date = new Date(g.submitted_at);
      // Only count grievances from the last 6 months
      if (date.getTime() > now.getTime() - (6 * 30 * 24 * 60 * 60 * 1000)) {
        const monthsAgo = (currentMonth - date.getMonth() + 12) % 12;
        if (monthsAgo < 6 && date.getFullYear() === currentYear) {
          monthlyData[5 - monthsAgo]++;
        }
      }
    });

    const trendsChart = new Chart(trendsChartCanvas, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Grievances',
          data: monthlyData,
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
            left: 10,
            right: 10,
            top: 10,
            bottom: 10
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1,
              color: '#e0e0e0',
              padding: 8,
              font: {
                size: 11
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
              padding: 8,
              maxRotation: 0,
              font: {
                size: 11
              }
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: '#e0e0e0',
              boxWidth: 12,
              padding: 15,
              font: {
                size: 11
              }
            }
          }
        }
      }
    });
    charts.push(trendsChart);
  }

  $effect(() => {
    if ($grievances && statusChartCanvas && trendsChartCanvas) {
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
      <p class="stat-number">{$grievances.length}</p>
    </div>
    <div class="stat-card">
      <h3>Resolved</h3>
      <p class="stat-number">
        {$grievances.filter(g => g.status === 'resolved').length}
      </p>
    </div>
    <div class="stat-card">
      <h3>Pending</h3>
      <p class="stat-number">
        {$grievances.filter(g => g.status === 'pending').length}
      </p>
    </div>
    <div class="stat-card">
      <h3>Stakeholders</h3>
      <p class="stat-number">{$stakeholders.length}</p>
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
        <KanbanBoard grievances={$grievances} />
      {:else}
        <GrievanceTable 
          grievances={$grievances}
          showColumns={['submitter_name', 'rank', 'unit', 'position', 'grievance_type', 'status', 'created_at']}
          canEditStatus={true}
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
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    width: 100%;
    height: 400px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .chart-card h3 {
    margin: 0 0 1.5rem 0;
    text-align: center;
    font-size: 1rem;
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
    max-width: 100%;
    height: calc(100% - 2.5rem);
    overflow: hidden;
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
    }

    .chart-card {
      height: 350px;
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