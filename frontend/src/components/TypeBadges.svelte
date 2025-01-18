<script>
  import { FileText } from 'lucide-svelte';
  
  let { type, subtype, showIcon = true } = $props();
</script>

<div class="type-info">
  {#if showIcon}
    <FileText size={14} />
  {/if}
  <span class="type-badge">{type}</span>
  {#if subtype}
    <span class="subtype-badge">{subtype}</span>
  {/if}
</div>

<style>
  .type-info {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .type-badge {
    background: var(--primary-dark, #1A1A1A);
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: capitalize;
    color: #64B5F6;
    border: 1px solid #64B5F6;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .subtype-badge {
    background: rgba(100, 181, 246, 0.1);
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: capitalize;
    color: #64B5F6;
    display: inline-flex;
    align-items: center;
  }
</style> 