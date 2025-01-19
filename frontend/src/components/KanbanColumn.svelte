<script>
  import Sortable from 'sortablejs';
  import KanbanCard from './KanbanCard.svelte';

  let columnEl;
  let sortable;

  let {
    title,
    status,
    grievances,
    handleStatusChange,
    onGrievanceSelect = $bindable()
  } = $props();

  $effect(() => {
    if (columnEl && !sortable) {
      sortable = new Sortable(columnEl, {
        group: 'grievances',
        animation: 150,
        ghostClass: 'ghost',
        sort: false,
        onEnd: async (evt) => {
          if (evt.from !== evt.to) {
            const grievanceId = evt.item.dataset.id;
            const newStatus = evt.to.closest('.column').dataset.status;
            const oldStatus = evt.from.closest('.column').dataset.status;
            
            if (newStatus !== oldStatus) {
              evt.item.remove();
              try {
                const success = await handleStatusChange(grievanceId, newStatus);
                if (!success) {
                  evt.from.appendChild(evt.item);
                }
              } catch (error) {
                console.error('Status change failed:', error);
                evt.from.appendChild(evt.item);
              }
            } else {
              evt.item.remove();
            }
          }
        }
      });
    }

    return () => {
      if (sortable) {
        sortable.destroy();
        sortable = null;
      }
    };
  });
</script>

<div class="kanban-column">
  <div class="column" data-status={status}>
    <div class="column-header">
      <h3>{title}</h3>
      <span class="count">{grievances.length}</span>
    </div>
    <div class="cards" bind:this={columnEl}>
      {#each grievances as grievance (grievance.id)}
        <div class="card-wrapper" data-id={grievance.id}>
          <KanbanCard {grievance} onSelect={onGrievanceSelect} />
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .kanban-column {
    background: #2d2d2d;
    border-radius: 8px;
    padding: 1rem;
    min-width: 300px;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .column {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 1rem;
    min-width: 300px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    flex: 1;
  }

  .column[data-status="pending"] {
    background: linear-gradient(rgba(255, 165, 0, 0.05), rgba(255, 165, 0, 0.05)), var(--gray-dark, #333333);
  }

  .column[data-status="in_progress"] {
    background: linear-gradient(rgba(100, 181, 246, 0.05), rgba(100, 181, 246, 0.05)), var(--gray-dark, #333333);
  }

  .column[data-status="resolved"] {
    background: linear-gradient(rgba(76, 175, 80, 0.05), rgba(76, 175, 80, 0.05)), var(--gray-dark, #333333);
  }

  .column-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    flex-shrink: 0;
  }

  .cards {
    flex: 1;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0.5rem;
    margin: -0.5rem;
  }

  h3 {
    margin: 0;
    font-size: 1.1rem;
  }

  .count {
    background: #3d3d3d;
    color: #e0e0e0;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.9rem;
  }

  :global(.ghost) {
    opacity: 0.5;
  }

  @media (max-width: 768px) {
    .kanban-column {
      padding: 0.75rem;
    }

    .column-header {
      margin-bottom: 0.75rem;
    }
  }

  .card-wrapper {
    width: 100%;
  }

  .card-wrapper.dragging {
    opacity: 0.5;
  }
</style> 