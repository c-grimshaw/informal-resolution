<script>
  import { createEventDispatcher } from 'svelte';

  const { view } = $props();
  const dispatch = createEventDispatcher();

  function toggleView() {
    dispatch('toggle', view === 'kanban' ? 'table' : 'kanban');
  }
</script>

<button class="view-toggle" onclick={toggleView}>
  {#if view === 'kanban'}
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
      <line x1="3" y1="9" x2="21" y2="9"></line>
      <line x1="3" y1="15" x2="21" y2="15"></line>
      <line x1="9" y1="9" x2="9" y2="21"></line>
      <line x1="15" y1="9" x2="15" y2="21"></line>
    </svg>
  {:else}
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <line x1="3" y1="6" x2="21" y2="6"></line>
      <line x1="3" y1="12" x2="21" y2="12"></line>
      <line x1="3" y1="18" x2="21" y2="18"></line>
    </svg>
  {/if}
  <span>{view === 'kanban' ? 'Switch to Table' : 'Switch to Kanban'}</span>
</button>

<style>
  .view-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
  }

  .view-toggle:hover {
    background: var(--gray-dark, #333333);
    border-color: var(--text-light, #FFFFFF);
  }

  .view-toggle svg {
    transition: transform 0.2s ease;
  }

  .view-toggle:hover svg {
    transform: scale(1.1);
  }
</style> 