<script>
  import { store } from '../lib/stores/store.svelte';
  import { put, del } from '../lib/api/client';
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
    Target,
    X
  } from 'lucide-svelte';
  import TypeBadges from './TypeBadges.svelte';
  import GrievanceModal from './GrievanceModal.svelte';

  const { 
    grievances,
    showColumns = ['rank', 'unit', 'position', 'grievance_type', 'status', 'created_at'],
    showFilters = true,
    canEditStatus = false,
    readonly = false,
    canDelete = false,
    onDelete = null
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
        const direction = sortDirection === 'asc' ? 1 : -1;
        
        if (sortField === 'created_at') {
          return direction * (new Date(a[sortField]).getTime() - new Date(b[sortField]).getTime());
        }
        
        const aVal = a[sortField].toLowerCase();
        const bVal = b[sortField].toLowerCase();
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
      store.setLoading(true);
      const updatedGrievance = {
        title: grievance.title,
        description: grievance.description,
        redress_sought: grievance.redress_sought,
        submitter_name: grievance.submitter_name,
        service_number: grievance.service_number,
        rank: grievance.rank,
        email: grievance.email,
        phone: grievance.phone,
        unit: grievance.unit,
        position: grievance.position,
        grievance_type: grievance.grievance_type,
        grievance_subtype: grievance.grievance_subtype,
        status: newStatus
      };
      
      const response = await put(`/grievances/${grievance.id}`, updatedGrievance);
      store.updateGrievance(grievance.id, response);
    } catch (error) {
      store.setError('Failed to update status');
    } finally {
      store.setLoading(false);
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

  function getStatusClass(status) {
    switch(status?.toLowerCase()) {
      case 'pending':
        return 'status-pending';
      case 'in_progress':
        return 'status-in-progress';
      case 'resolved':
        return 'status-resolved';
      default:
        return '';
    }
  }

  async function handleDelete(grievance, event) {
    event.stopPropagation(); // Prevent row click
    
    if (!confirm('Are you sure you want to delete this grievance? This action cannot be undone.')) {
      return;
    }

    try {
      await del(`/grievances/${grievance.id}`);
      store.deleteGrievance(grievance.id);
      if (onDelete) {
        onDelete(grievance.id);
      }
    } catch (error) {
      store.setError('Failed to delete grievance');
    }
  }
</script>

<div class="table-container" class:modal-open={showModal}>
  {#if showFilters}
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
    <div class="filter-group">
      <AlertCircle size={16} />
      <select 
        bind:value={filters.status}
        class="filter-select"
      >
        <option value="">All Statuses</option>
        {#each statusOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
  </div>
  {/if}

  <div class="table-scroll">
    <table>
      <thead>
        <tr>
          {#each columns as column}
            <th onclick={() => toggleSort(column.field)}>
              <div class="th-content">
                {#if column.icon}
                    {@const Icon = column.icon}
                    <Icon size={16} />
                {/if}
                <span>{column.label}</span>
                {#if sortField === column.field}
                  {@const SortIcon = sortDirection === 'asc' ? ArrowUp : ArrowDown}
                  <SortIcon size={16} class="sort-indicator" />
                {/if}
              </div>
            </th>
          {/each}
          {#if canDelete}
            <th></th>
          {/if}
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
                    {#if grievance.status}
                    {@const StatusIcon = getStatusIcon(grievance.status)}
                    <StatusIcon size={16} class="status-icon {grievance.status}" />
                    {/if}
                    {#if canEditStatus && !readonly}
                      <select 
                        value={grievance.status}
                        onchange={(e) => handleStatusChange(grievance, e.currentTarget.value)}
                        class="status-select"
                        class:status-pending={grievance.status === 'pending'}
                        class:status-in-progress={grievance.status === 'in_progress'}
                        class:status-resolved={grievance.status === 'resolved'}
                      >
                        {#each statusOptions as option}
                          <option value={option.value}>{option.label}</option>
                        {/each}
                      </select>
                    {:else}
                      <span class="status-badge {getStatusClass(grievance.status)}">
                        {grievance.status.replace('_', ' ')}
                      </span>
                    {/if}
                  </div>
                {:else if column.field === 'created_at'}
                  {formatDate(grievance[column.field])}
                {:else}
                  {grievance[column.field]}
                {/if}
              </td>
            {/each}
            {#if canDelete}
              <td class="delete-cell">
                <button 
                  class="delete-btn"
                  onclick={(e) => handleDelete(grievance, e)}
                  title="Delete grievance"
                >
                  <X size={16} />
                </button>
              </td>
            {/if}
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
    cursor: pointer;
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

  .filter-group select {
    width: 100%;
    padding: 8px 0;
    background: transparent;
    border: none;
    color: var(--text-light, #FFFFFF);
    font-size: 0.9em;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 8px center;
    background-size: 16px;
    padding-right: 32px;
  }

  .filter-group select:focus {
    outline: none;
  }

  .filter-group select option {
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    padding: 8px;
  }

  .status-select {
    width: 140px;
    padding: 6px 12px;
    border-radius: 4px;
    background-color: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    border: 1px solid var(--gray-medium, #666666);
    cursor: pointer;
    font-size: 0.85em;
    font-weight: 500;
    text-transform: capitalize;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat !important;
    background-position: calc(100% - 8px) center !important;
    background-size: 16px;
    padding-right: 32px;
    transition: all 0.2s ease;
  }

  .status-select.status-pending {
    border-color: #FFA500;
    color: #FFA500;
    background-color: rgba(255, 165, 0, 0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23FFA500' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }

  .status-select.status-in-progress {
    border-color: #64B5F6;
    color: #64B5F6;
    background-color: rgba(100, 181, 246, 0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2364B5F6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }

  .status-select.status-resolved {
    border-color: #4CAF50;
    color: #4CAF50;
    background-color: rgba(76, 175, 80, 0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%234CAF50' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }

  .status-select:hover {
    border-color: var(--text-light, #FFFFFF);
  }

  .status-select:focus {
    outline: none;
    border-color: var(--text-light, #FFFFFF);
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
  }

  .status-select option {
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    padding: 8px;
  }

  .status-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .status-badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.9em;
    text-transform: capitalize;
    font-weight: 500;
    min-width: 100px;
    text-align: center;
  }

  .status-pending {
    background: rgba(255, 165, 0, 0.2);
    color: #FFA500;
    border: 1px solid #FFA500;
  }

  .status-in-progress {
    background: rgba(100, 181, 246, 0.2);
    color: #64B5F6;
    border: 1px solid #64B5F6;
  }

  .status-resolved {
    background: rgba(76, 175, 80, 0.2);
    color: #4CAF50;
    border: 1px solid #4CAF50;
  }

  .status-icon {
    opacity: 0.8;
  }

  .status-icon.pending {
    color: #FFA500;
  }

  .status-icon.in_progress {
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

  .delete-cell {
    width: 40px;
    text-align: center;
  }

  .delete-btn {
    background: transparent;
    border: none;
    color: #ff5252;
    padding: 4px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .delete-btn:hover {
    background: rgba(255, 82, 82, 0.1);
    color: #ff7070;
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
</style> 