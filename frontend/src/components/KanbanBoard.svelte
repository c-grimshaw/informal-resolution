<script>
  import { actions } from '../lib/stores/store';
  import { put } from '../lib/api/client';
  import KanbanColumn from './KanbanColumn.svelte';

  const { grievances } = $props();

  const columns = [
    { title: 'Pending', status: 'pending' },
    { title: 'In Progress', status: 'in_progress' },
    { title: 'Resolved', status: 'resolved' }
  ];

  const columnGrievances = (status) => 
    grievances.filter(g => g.status === status);

  async function handleStatusChange(grievanceId, newStatus) {
    try {
      const grievance = grievances.find(g => g.id === grievanceId);
      if (!grievance) return;

      console.log('Original grievance:', grievance);

      const updatedGrievance = {
        name: grievance.name || '',
        serviceNumber: grievance.serviceNumber || '',
        rank: grievance.rank || '',
        email: grievance.email || '',
        phone: grievance.phone || '',
        unit: grievance.unit || '',
        position: grievance.position || '',
        grievanceType: grievance.grievanceType || grievance.grievance_type || '',
        grievanceSubType: grievance.grievanceSubType || grievance.grievance_subtype || '',
        description: grievance.description || '',
        status: newStatus
      };

      console.log('Updating grievance with data:', JSON.stringify(updatedGrievance, null, 2));
      
      // Set loading state
      actions.setLoading(true);
      
      try {
        const response = await put(`/grievances/${grievanceId}`, updatedGrievance);
        console.log('Response:', response);
        
        // Only update the store if we got a valid response
        if (response && response.id) {
          // Update the store with the response data
          actions.updateGrievance(grievanceId, response);
        } else {
          throw new Error('Invalid response from server');
        }
      } catch (apiError) {
        console.error('API Error:', apiError);
        console.error('API Error Response:', apiError.response);
        console.error('API Error Data:', apiError.response?.data);
        console.error('API Error Status:', apiError.response?.status);
        throw apiError;
      } finally {
        actions.setLoading(false);
      }
    } catch (error) {
      console.error('Failed to update grievance status:', error);
      console.error('Error details:', error.response?.data || error.message);
      actions.setError('Failed to update status');
    }
  }
</script>

<div class="kanban-board">
  {#each columns as column}
    <KanbanColumn
      title={column.title}
      status={column.status}
      grievances={columnGrievances(column.status)}
      {handleStatusChange}
    />
  {/each}
</div>

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