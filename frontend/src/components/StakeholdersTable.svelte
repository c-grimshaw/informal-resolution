<script>
  import { store } from '../lib/stores/store.svelte';
  import { auth } from '../lib/stores/authStore.svelte';
  import { patch } from '../lib/api/client';
  import { 
    ArrowUp,
    ArrowDown,
    User, 
    Building2,
    Mail,
    Shield,
    Medal,
    Target
  } from 'lucide-svelte';

  let { 
    stakeholders = [],
    showFilters = true
  } = $props();

  const roleOptions = [
    { value: 'user', label: 'User' },
    { value: 'supervisor', label: 'Supervisor' },
    { value: 'admin', label: 'Admin' }
  ];

  // Define all possible columns
  const columns = [
    { field: 'email', label: 'Email', icon: Mail },
    { field: 'name', label: 'Name', icon: User },
    { field: 'rank', label: 'Rank', icon: Medal },
    { field: 'unit', label: 'Unit', icon: Building2 },
    { field: 'position', label: 'Position', icon: Target },
    { field: 'role', label: 'Role', icon: Shield }
  ];

  let sortField = $state('email');
  let sortDirection = $state('asc');
  let filters = $state({
    email: '',
    name: '',
    unit: '',
    role: ''
  });

  let sortedAndFilteredStakeholders = $derived(
    stakeholders
      .filter(s => {
        return (!filters.email || s.email.toLowerCase().includes(filters.email.toLowerCase())) &&
               (!filters.name || s.name?.toLowerCase().includes(filters.name.toLowerCase())) &&
               (!filters.unit || s.unit?.toLowerCase().includes(filters.unit.toLowerCase())) &&
               (!filters.role || s.role?.toLowerCase().includes(filters.role.toLowerCase()));
      })
      .sort((a, b) => {
        const direction = sortDirection === 'asc' ? 1 : -1;
        const aVal = (a[sortField] || '').toLowerCase();
        const bVal = (b[sortField] || '').toLowerCase();
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

  async function handleRoleChange(stakeholder, newRole) {
    try {
      store.setLoading(true);
      console.log('Attempting role change:', { userId: stakeholder.id, newRole });
      const response = await patch(`/users/${stakeholder.id}`, {
        role: newRole
      });
      console.log('Role change response:', response);
      
      // Update the stakeholder in the local state
      stakeholders = stakeholders.map(s => 
        s.id === stakeholder.id ? { ...s, role: newRole } : s
      );
      // If this is the current user, update the auth store
      if (stakeholder.id === auth.user?.id) {
        auth.setUser({ ...auth.user, role: newRole });
      }
      store.setError('✓ Role updated successfully');
    } catch (error) {
      console.error('Role change error:', error);
      store.setError('Failed to update role: ' + error.message);
    } finally {
      store.setLoading(false);
    }
  }

  function getRoleBadgeClass(role) {
    switch(role?.toLowerCase()) {
      case 'admin':
        return 'role-admin';
      case 'supervisor':
        return 'role-supervisor';
      default:
        return 'role-user';
    }
  }
</script>

<div class="table-container">
  {#if showFilters}
    <div class="filters">
      <div class="filter-group">
        <Mail size={16} />
        <input 
          type="text" 
          placeholder="Filter by email..." 
          bind:value={filters.email}
          class="filter-input"
        >
      </div>
      <div class="filter-group">
        <User size={16} />
        <input 
          type="text" 
          placeholder="Filter by name..." 
          bind:value={filters.name}
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
        <Shield size={16} />
        <input 
          type="text" 
          placeholder="Filter by role..." 
          bind:value={filters.role}
          class="filter-input"
        >
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
        </tr>
      </thead>
      <tbody>
        {#each sortedAndFilteredStakeholders as stakeholder (stakeholder.id)}
          <tr>
            {#each columns as column}
              <td>
                {#if column.field === 'role'}
                  {#if auth.isAdmin && stakeholder.id !== auth.user?.id}
                    <select 
                      value={stakeholder[column.field]}
                      onchange={(e) => handleRoleChange(stakeholder, e.currentTarget.value)}
                      class="role-select {getRoleBadgeClass(stakeholder[column.field])}"
                    >
                      {#each roleOptions as option}
                        <option value={option.value}>{option.label}</option>
                      {/each}
                    </select>
                  {:else}
                    <span class="role-badge {getRoleBadgeClass(stakeholder[column.field])}">
                      {stakeholder[column.field]}
                    </span>
                  {/if}
                {:else}
                  {stakeholder[column.field]}
                {/if}
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

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

  .filter-input {
    width: 100%;
    padding: 8px 0;
    background: transparent;
    border: none;
    color: var(--text-light, #FFFFFF);
    font-size: 0.9em;
  }

  .filter-input:focus {
    outline: none;
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

  tr:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .role-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: 500;
    text-transform: capitalize;
  }

  .role-admin {
    background: rgba(244, 67, 54, 0.2);
    color: #F44336;
    border: 1px solid #F44336;
  }

  .role-supervisor {
    background: rgba(33, 150, 243, 0.2);
    color: #2196F3;
    border: 1px solid #2196F3;
  }

  .role-user {
    background: rgba(76, 175, 80, 0.2);
    color: #4CAF50;
    border: 1px solid #4CAF50;
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

  .role-select {
    width: 140px;
    padding: 6px 12px;
    border-radius: 4px;
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    border: 1px solid var(--gray-medium, #666666);
    cursor: pointer;
    font-size: 0.85em;
    font-weight: 500;
    text-transform: capitalize;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 8px center;
    background-size: 16px;
    padding-right: 32px;
    transition: all 0.2s ease;
  }

  .role-select:hover {
    border-color: var(--text-light, #FFFFFF);
  }

  .role-select:focus {
    outline: none;
    border-color: var(--text-light, #FFFFFF);
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
  }

  .role-select.role-admin {
    border-color: #F44336;
    color: #F44336;
    background-color: rgba(244, 67, 54, 0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23F44336' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }

  .role-select.role-admin:hover,
  .role-select.role-admin:focus {
    border-color: #F44336;
    box-shadow: 0 0 0 2px rgba(244, 67, 54, 0.2);
  }

  .role-select.role-supervisor {
    border-color: #2196F3;
    color: #2196F3;
    background-color: rgba(33, 150, 243, 0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%232196F3' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }

  .role-select.role-supervisor:hover,
  .role-select.role-supervisor:focus {
    border-color: #2196F3;
    box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
  }

  .role-select.role-user {
    border-color: #4CAF50;
    color: #4CAF50;
    background-color: rgba(76, 175, 80, 0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%234CAF50' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }

  .role-select.role-user:hover,
  .role-select.role-user:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
  }

  .role-select option {
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    padding: 8px;
  }

  @media (max-width: 768px) {
    .filters {
      grid-template-columns: 1fr;
    }

    th, td {
      padding: 8px 12px;
    }

    .table-container {
      height: calc(100vh - 200px);
    }
  }
</style> 