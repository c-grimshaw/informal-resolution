<script>
  import { actions, loading } from '../lib/stores/store';
  import { put } from '../lib/api/client';
  import { 
    ArrowUp,
    ArrowDown,
    User, 
    Building2, 
    FileText, 
    Clock,
    AlertCircle,
    CheckCircle2,
    Timer,
    Medal,
    Target
  } from 'lucide-svelte';
  import TypeBadges from './TypeBadges.svelte';
  import GrievanceModal from './GrievanceModal.svelte';

  const { 
    grievances,
    showColumns = ['rank', 'unit', 'position', 'grievance_type', 'status', 'created_at'],
    canEditStatus = false 
  } = $props();

  // Define all possible columns
  const allColumns = {
    submitter_name: { field: 'submitter_name', label: 'Name', icon: User },
    rank: { field: 'rank', label: 'Rank', icon: Medal },
    unit: { field: 'unit', label: 'Unit', icon: Building2 },
    position: { field: 'position', label: 'Position', icon: Target },
    grievance_type: { field: 'grievance_type', label: 'Type', icon: FileText },
    status: { field: 'status', label: 'Status', icon: null },
    created_at: { field: 'created_at', label: 'Date', icon: Clock }
  };

  // Filter columns based on showColumns prop
  const columns = showColumns.map(col => allColumns[col]).filter(Boolean);

  let selectedGrievance = $state(null);
  let showModal = $state(false);

  const statusOptions = [
    { value: 'pending', label: 'Pending' },
    { value: 'in_progress', label: 'In Progress' },
    { value: 'resolved', label: 'Resolved' }
  ];

  let sortField = $state('created_at');
  let sortDirection = $state('desc');
  let filters = $state({
    submitter_name: '',
    unit: '',
    type: '',
    status: ''
  });

  let sortedAndFilteredGrievances = $derived(
    grievances
      .filter(g => {
        return (!filters.submitter_name || g.submitter_name.toLowerCase().includes(filters.submitter_name.toLowerCase())) &&
               (!filters.unit || g.unit.toLowerCase().includes(filters.unit.toLowerCase())) &&
               (!filters.type || 
                 g.grievance_type?.toLowerCase().includes(filters.type.toLowerCase()) ||
                 g.grievance_subtype?.toLowerCase().includes(filters.type.toLowerCase())
               ) &&
               (!filters.status || g.status === filters.status);
      })
      .sort((a, b) => {
        const aVal = a[sortField];
        const bVal = b[sortField];
        const direction = sortDirection === 'asc' ? 1 : -1;

        if (sortField === 'created_at') {
          return direction * (new Date(aVal).getTime() - new Date(bVal).getTime());
        }
        
        return direction * (aVal < bVal ? -1 : aVal > bVal ? 1 : 0);
      })
  );

  function toggleSort(field) {
    if (sortField === field) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortField = field;
      sortDirection = 'asc';
    }
  }

  async function handleStatusChange(grievance, newStatus) {
    try {
      $loading = true;
      const updatedGrievance = {
        name: grievance.name,
        serviceNumber: grievance.serviceNumber,
        rank: grievance.rank,
        email: grievance.email,
        phone: grievance.phone,
        unit: grievance.unit,
        position: grievance.position,
        grievanceType: grievance.grievanceType,
        grievanceSubType: grievance.grievanceSubType,
        description: grievance.description,
        status: newStatus
      };
      
      const response = await put(`/grievances/${grievance.id}`, updatedGrievance);
      actions.updateGrievance(grievance.id, response);
    } catch (error) {
      actions.setError('Failed to update status');
    } finally {
      $loading = false;
    }
  }

  function getStatusIcon(status) {
    switch(status) {
      case 'pending':
        return AlertCircle;
      case 'in_progress':
        return Timer;
      case 'resolved':
        return CheckCircle2;
      default:
        return AlertCircle;
    }
  }

  function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Invalid Date';
      return new Intl.DateTimeFormat('en-CA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    } catch (error) {
      console.error('Error formatting date:', error);
      return 'Invalid Date';
    }
  }

  function handleRowClick(grievance, event) {
    if (event.target.closest('.status-select')) return;
    selectedGrievance = grievance;
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    selectedGrievance = null;
  }
</script>

<div class="table-container" class:modal-open={showModal}>
  <div class="filters">
    <div class="filter-group">
      <User size={16} />
      <input 
        type="text" 
        placeholder="Filter by name..." 
        bind:value={filters.submitter_name}
        class="filter-input"
      >
    </div>
    <div class="filter-group">
      <Building2 size={16} />
      <input 
        type="text" 
        placeholder="Filter by unit..." 
        bind:value={filters.unit}
        class="filter-input"
      >
    </div>
    <div class="filter-group">
      <FileText size={16} />
      <input 
        type="text" 
        placeholder="Filter by type..." 
        bind:value={filters.type}
        class="filter-input"
      >
    </div>
    <select 
      bind:value={filters.status}
      class="filter-input"
    >
      <option value="">All Statuses</option>
      {#each statusOptions as option}
        <option value={option.value}>{option.label}</option>
      {/each}
    </select>
  </div>

  <div class="table-scroll">
    <table>
      <thead>
        <tr>
          {#each columns as column}
            <th onclick={() => toggleSort(column.field)}>
              <div class="th-content">
                {#if column.icon}
                  <svelte:component this={column.icon} size={16} />
                {/if}
                <span>{column.label}</span>
                {#if sortField === column.field}
                  <svelte:component 
                    this={sortDirection === 'asc' ? ArrowUp : ArrowDown} 
                    size={16} 
                    class="sort-indicator" 
                  />
                {/if}
              </div>
            </th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each sortedAndFilteredGrievances as grievance (grievance.id)}
          <tr onclick={(e) => handleRowClick(grievance, e)}>
            {#each columns as column}
              <td>
                {#if column.field === 'grievance_type'}
                  <TypeBadges 
                    type={grievance.grievance_type} 
                    subtype={grievance.grievance_subtype}
                    showIcon={false}
                  />
                {:else if column.field === 'status'}
                  <div class="status-container">
                    <svelte:component this={getStatusIcon(grievance.status)} size={16} class="status-icon {grievance.status}" />
                    {#if canEditStatus}
                      <select 
                        value={grievance.status}
                        onchange={(e) => handleStatusChange(grievance, e.currentTarget.value)}
                        class="status-select"
                        class:pending={grievance.status === 'pending'}
                        class:in-progress={grievance.status === 'in_progress'}
                        class:resolved={grievance.status === 'resolved'}
                      >
                        {#each statusOptions as option}
                          <option value={option.value}>{option.label}</option>
                        {/each}
                      </select>
                    {:else}
                      <span class="status-text">{grievance.status.replace('_', ' ')}</span>
                    {/if}
                  </div>
                {:else if column.field === 'created_at'}
                  {formatDate(grievance[column.field])}
                {:else}
                  {grievance[column.field]}
                {/if}
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<GrievanceModal 
  grievance={selectedGrievance}
  isOpen={showModal}
  closeModal={() => {
    showModal = false;
    selectedGrievance = null;
  }}
/>

<style>
  .table-container {
    width: 100%;
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 250px);
  }

  .filters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    padding: 1rem;
    background: var(--primary-dark, #1A1A1A);
    border-bottom: 1px solid var(--gray-medium, #666666);
  }

  .filter-input {
    width: 100%;
    padding: 8px 12px;
    background: var(--gray-dark, #333333);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 4px;
    color: var(--text-light, #FFFFFF);
    font-size: 0.9em;
  }

  .filter-input:focus {
    outline: none;
    border-color: var(--text-light, #FFFFFF);
  }

  .table-scroll {
    flex: 1;
    overflow-y: auto;
    min-height: 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    color: var(--text-light, #FFFFFF);
  }

  thead {
    position: sticky;
    top: 0;
    background: var(--primary-dark, #1A1A1A);
    z-index: 1;
  }

  th, td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--gray-medium, #666666);
  }

  th {
    background: var(--primary-dark, #1A1A1A);
    font-weight: 500;
    text-transform: uppercase;
    font-size: 0.8em;
    letter-spacing: 1px;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
  }

  th:hover {
    background: var(--gray-dark, #333333);
  }

  .sort-indicator {
    margin-left: 4px;
    color: var(--primary-red, #C41E3A);
  }

  tr:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .description-cell {
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .type-badge {
    background: var(--primary-dark, #1A1A1A);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    margin-right: 4px;
  }

  .subtype-badge {
    background: var(--gray-medium, #666666);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
  }

  .status-select {
    width: 140px;
    padding: 6px 12px;
    border-radius: 4px;
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    border: 1px solid var(--gray-medium, #666666);
    cursor: pointer;
    font-size: 0.9em;
  }

  .status-select:focus {
    outline: none;
    border-color: var(--text-light, #FFFFFF);
  }

  .status-select.pending {
    border-color: #FFA500;
  }

  .status-select.in-progress {
    border-color: #64B5F6;
  }

  .status-select.resolved {
    border-color: #4CAF50;
  }

  @media (max-width: 768px) {
    .filters {
      grid-template-columns: 1fr;
    }

    .description-cell {
      max-width: 150px;
    }

    th, td {
      padding: 8px 12px;
    }

    .type-badge, .subtype-badge {
      display: block;
      margin: 2px 0;
    }

    .table-container {
      height: calc(100vh - 200px);
    }
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--gray-dark, #333333);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 4px;
    padding: 0 0.75rem;
  }

  .filter-group :global(svg) {
    color: var(--gray-medium, #666666);
  }

  .filter-group .filter-input {
    border: none;
    background: transparent;
    padding: 8px 0;
  }

  .filter-group .filter-input:focus {
    outline: none;
  }

  .th-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .th-content :global(svg) {
    color: var(--gray-medium, #666666);
  }

  .sort-indicator {
    color: var(--primary-red, #C41E3A);
  }

  .status-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .status-icon {
    min-width: 16px;
  }

  .status-icon.pending {
    color: #FFA500;
  }

  .status-icon.in-progress {
    color: #64B5F6;
  }

  .status-icon.resolved {
    color: #4CAF50;
  }

  .table-container.modal-open {
    filter: blur(4px);
    pointer-events: none;
  }

  .table-container.modal-open .table-scroll {
    overflow: hidden;
  }
</style> 