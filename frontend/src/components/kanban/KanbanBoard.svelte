<script>
  import { store } from '../../lib/stores/store.svelte';
  import { put } from '../../lib/api/client';
  import KanbanColumn from './KanbanColumn.svelte';
  import GrievanceModal from '../GrievanceModal.svelte';

  let selectedGrievance = $state(null);
  let localGrievances = $state(store.grievances);

  // Keep local state in sync with store
  $effect(() => {
    localGrievances = store.grievances;
  });

  const columns = [
    { title: 'Pending', status: 'pending' },
    { title: 'In Progress', status: 'in_progress' },
    { title: 'Resolved', status: 'resolved' }
  ];

  function getGrievancesForStatus(status) {
    return localGrievances.filter(g => g.status === status);
  }

  function handleGrievanceSelect(grievance) {
    selectedGrievance = grievance;
  }

  function closeModal() {
    selectedGrievance = null;
  }

  async function handleStatusChange(grievanceId, newStatus) {
    try {
      store.setLoading(true);
      
      const grievance = localGrievances.find(g => g.id === grievanceId);
      if (!grievance) {
        console.error('Grievance not found:', grievanceId);
        return false;
      }
      
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
      
      const response = await put(`/grievances/${grievanceId}`, updatedGrievance);
      
      // Update local state first
      localGrievances = localGrievances.map(g => 
        g.id === grievanceId ? { ...g, status: newStatus } : g
      );
      
      // Then update store
      store.updateGrievance(grievanceId, response);
      return true;
    } catch (error) {
      console.error('Status update failed:', error);
      store.setError('Failed to update status');
      return false;
    } finally {
      store.setLoading(false);
    }
  }
</script>

<div class="kanban-board">
  {#each columns as column}
    <KanbanColumn
      title={column.title}
      status={column.status}
      grievances={getGrievancesForStatus(column.status)}
      {handleStatusChange}
      onGrievanceSelect={handleGrievanceSelect}
    />
  {/each}
</div>

<GrievanceModal 
  grievance={selectedGrievance}
  isOpen={selectedGrievance !== null}
  {closeModal}
/>

<style>
  .kanban-board {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    padding: 1rem;
    height: calc(100vh - 250px);
    min-height: 600px;
    overflow-x: auto;
  }

  @media (min-width: 1200px) {
    .kanban-board {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  @media (max-width: 768px) {
    .kanban-board {
      height: calc(100vh - 200px);
      padding: 0.5rem;
      gap: 0.5rem;
    }
  }
</style> 