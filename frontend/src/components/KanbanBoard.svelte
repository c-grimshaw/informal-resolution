<script>
  import { store } from '../lib/stores/store.svelte';
  import { put } from '../lib/api/client';
  import KanbanColumn from './KanbanColumn.svelte';
  import GrievanceModal from './GrievanceModal.svelte';

  const { grievances } = $props();
  let selectedGrievance = $state(null);

  const columns = [
    { title: 'Pending', status: 'pending' },
    { title: 'In Progress', status: 'in_progress' },
    { title: 'Resolved', status: 'resolved' }
  ];

  function getGrievancesForStatus(status) {
    return store.grievances.filter(g => g.status === status);
  }

  function handleGrievanceSelect(grievance) {
    selectedGrievance = grievance;
  }

  function closeModal() {
    selectedGrievance = null;
  }

  async function handleStatusChange(grievanceId, newStatus) {
    try {
      console.log(`handleStatusChange called with id: ${grievanceId}, newStatus: ${newStatus}`);
      store.setLoading(true);
      
      const grievance = store.grievances.find(g => g.id === grievanceId);
      if (!grievance) {
        console.error('Grievance not found:', grievanceId);
        return false;
      }
      
      console.log('Found grievance:', grievance);
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
      
      console.log('Sending update to API:', updatedGrievance);
      const response = await put(`/grievances/${grievanceId}`, updatedGrievance);
      console.log('API response:', response);
      
      store.updateGrievance(grievanceId, response);
      console.log('Store updated successfully');
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