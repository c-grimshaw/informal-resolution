<script>
  import { FileText } from 'lucide-svelte';
  
  let { type = '', subtype = '', showIcon = true } = $props();

  const typeColors = {
    'administrative': { bg: '#FF9800', color: '#FFF3E0' },
    'disciplinary': { bg: '#F44336', color: '#FFEBEE' },
    'workplace': { bg: '#4CAF50', color: '#E8F5E9' },
    'benefits': { bg: '#2196F3', color: '#E3F2FD' },
    'harassment': { bg: '#9C27B0', color: '#F3E5F5' },
    'discrimination': { bg: '#E91E63', color: '#FCE4EC' },
    'performance': { bg: '#FF5722', color: '#FBE9E7' },
    'other': { bg: '#607D8B', color: '#ECEFF1' }
  };

  function getTypeColor(type) {
    const normalizedType = type?.toLowerCase() || 'other';
    return typeColors[normalizedType] || typeColors.other;
  }
</script>

{#if type}
  <div class="badge-container">
    <div class="type-badge" style="--badge-bg: {getTypeColor(type).bg}; --badge-color: {getTypeColor(type).color}">
      {#if showIcon}
        <FileText size={14} />
      {/if}
      <span>{type}</span>
    </div>
    {#if subtype}
      <div class="subtype-badge">
        <span>{subtype}</span>
      </div>
    {/if}
  </div>
{/if}

<style>
  .badge-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .type-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: 500;
    background: var(--badge-bg);
    color: var(--badge-color);
  }

  .type-badge :global(svg) {
    opacity: 0.9;
  }

  .subtype-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-light, #FFFFFF);
    opacity: 0.8;
  }
</style> 