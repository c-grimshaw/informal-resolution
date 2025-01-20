<script>
  import { 
    User, 
    Building2, 
    AlertCircle,
    CheckCircle2,
    Timer,
    Phone,
    Mail,
    Medal,
    Target
  } from 'lucide-svelte';
  import TypeBadges from './TypeBadges.svelte';

  let { grievance, onSelect = $bindable() } = $props();

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
        day: 'numeric'
      }).format(date);
    } catch (error) {
      console.error('Error formatting date:', error);
      return 'Invalid Date';
    }
  }

  function handleCardClick() {
    onSelect(grievance);
  }
</script>

<div class="kanban-card" data-id={grievance.id} onclick={handleCardClick}>
  <div class="card-header">
    <div class="title">{grievance.title}</div>
    <div class="personal-info">
      <div class="info-item">
        <User size={14} />
        <span>{grievance.submitter_name}</span>
      </div>
      <div class="info-item">
        <Medal size={14} />
        <span>{grievance.rank}</span>
      </div>
      <div class="info-item">
        <Mail size={14} />
        <span>{grievance.email}</span>
      </div>
      <div class="info-item">
        <Phone size={14} />
        <span>{grievance.phone}</span>
      </div>
    </div>
    <div class="unit-info">
      <div class="info-item">
        <Building2 size={14} />
        <span>{grievance.unit}</span>
      </div>
      <div class="info-item">
        <Target size={14} />
        <span>{grievance.position}</span>
      </div>
    </div>
  </div>
  
  <div class="card-content">
    <TypeBadges 
      type={grievance.grievance_type} 
      subtype={grievance.grievance_subtype} 
    />
    <div class="content-section">
      <h4>Description:</h4>
      <p class="description">{grievance.description}</p>
    </div>
    <div class="content-section">
      <h4>Redress Sought:</h4>
      <p class="redress">{grievance.redress_sought}</p>
    </div>
  </div>

  <div class="card-footer">
    <div class="status">
      {#if grievance.status}
        {@const Icon = getStatusIcon(grievance.status)}
        <Icon size={14} class="status-icon {grievance.status}" />
      {/if}
      <span class="status-text">{grievance.status.replace('_', ' ')}</span>
    </div>
    <div class="date">
      {formatDate(grievance.created_at)}
    </div>
  </div>
</div>

<style>
  .kanban-card {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease;
    transform-origin: center;
    position: relative;
    overflow: hidden;
  }

  .kanban-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      transparent 0%,
      rgba(255, 255, 255, 0.03) 50%,
      transparent 100%
    );
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .kanban-card:hover {
    transform: scale(1.005);
    z-index: 1;
  }

  .kanban-card:hover::before {
    transform: translateX(100%);
  }

  .card-header {
    position: relative;
    margin-bottom: 0.75rem;
  }

  .unit-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-light, #FFFFFF);
    font-size: 0.9em;
  }

  .unit-info {
    margin-top: 0.25rem;
    opacity: 0.8;
  }

  .description {
    color: var(--text-light, #FFFFFF);
    font-size: 0.9em;
    margin: 0.5rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.75rem;
    font-size: 0.8em;
  }

  .status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .status-text {
    text-transform: capitalize;
  }

  .date {
    opacity: 0.7;
  }

  .kanban-card:active {
    cursor: grabbing;
  }

  .title {
    font-size: 1.1em;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: var(--text-light, #FFFFFF);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .personal-info, .unit-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .info-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-light, #FFFFFF);
    font-size: 0.85em;
    opacity: 0.9;
    min-width: 0;
  }

  .info-item span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
  }

  .content-section {
    margin: 0.75rem 0;
  }

  .content-section h4 {
    font-size: 0.9em;
    color: var(--text-light, #FFFFFF);
    margin: 0 0 0.25rem 0;
    opacity: 0.8;
  }

  .description, .redress {
    font-size: 0.9em;
    line-height: 1.4;
    color: var(--text-light, #FFFFFF);
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .redress {
    -webkit-line-clamp: 2;
    line-clamp: 2;
    opacity: 0.8;
  }
</style> 