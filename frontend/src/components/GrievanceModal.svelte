<script>
  import { 
    User, 
    Building2, 
    Phone,
    Mail,
    Medal,
    Briefcase,
    X,
    Hash,
  } from 'lucide-svelte';
  import TypeBadges from './TypeBadges.svelte';
  import GrievanceNotes from './GrievanceNotes.svelte';
  import { store } from '../lib/stores/store.svelte';
  import { get } from '../lib/api/client';
  import { slide } from 'svelte/transition';
  
  let { grievance = null, isOpen = false, closeModal = $bindable() } = $props();
  let notes = $state([]);

  async function loadNotes() {
    if (!grievance) return;
    try {
      const response = await get(`/grievances/${grievance.id}/notes`);
      notes = response;
    } catch (error) {
      store.setError('Failed to load notes: ' + error.message);
    }
  }

  function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-CA', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  }

  $effect(() => {
    if (grievance?.id) {
      loadNotes();
    }
  });

  function handleBackdropClick(event) {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }

  function handleCloseClick() {
    closeModal();
  }

</script>

{#if isOpen}
  <div class="modal-backdrop" 
    role="dialog"
    aria-modal="true"
    onclick={handleBackdropClick}
    onkeydown={(e) => e.key === 'Escape' && closeModal()}
  >
    <div class="modal-content" 
      onclick={(e) => e.stopPropagation()}
      transition:slide
    >
      <button class="close-button" onclick={handleCloseClick}>
        <X size={24} />
      </button>

      <div class="modal-header">
        <h2>Grievance Details</h2>
        <div class="submission-date">
          Submitted on {formatDate(grievance.created_at)}
        </div>
      </div>

      <div class="modal-body">
        <div class="info-section">
          <h3>Personal Information</h3>
          <div class="info-grid">
            <div class="info-item">
              <User size={16} />
              <span class="label">Name:</span>
              <span>{grievance.submitter_name}</span>
            </div>
            <div class="info-item">
              <Hash size={16} />
              <span class="label">Service Number:</span>
              <span>{grievance.service_number}</span>
            </div>
            <div class="info-item">
              <Medal size={16} />
              <span class="label">Rank:</span>
              <span>{grievance.rank}</span>
            </div>
            <div class="info-item">
              <Building2 size={16} />
              <span class="label">Unit:</span>
              <span>{grievance.unit}</span>
            </div>
            <div class="info-item">
              <Briefcase size={16} />
              <span class="label">Position:</span>
              <span>{grievance.position}</span>
            </div>
            <div class="info-item">
              <Mail size={16} />
              <span class="label">Email:</span>
              <span>{grievance.email}</span>
            </div>
            <div class="info-item">
              <Phone size={16} />
              <span class="label">Phone:</span>
              <span>{grievance.phone}</span>
            </div>
          </div>
        </div>

        <div class="info-section">
          <h3>Grievance Information</h3>
          <div class="grievance-type">
            <TypeBadges 
              type={grievance.grievance_type} 
              subtype={grievance.grievance_subtype}
            />
          </div>
          <div class="description">
            <h4>Description</h4>
            <p>{grievance.description}</p>
          </div>
          <div class="redress">
            <h4>Redress Requested</h4>
            <p>{grievance.redress_sought || 'No redress specified'}</p>
          </div>
        </div>

        <hr class="divider" />

        <GrievanceNotes grievanceId={grievance.id} />
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
    animation: fadeIn 0.2s ease-out;
  }

  .modal-content {
    background: var(--gray-dark, #333333);
    border-radius: 12px;
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    text-align: left;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      backdrop-filter: blur(0px);
      -webkit-backdrop-filter: blur(0px);
    }
    to {
      opacity: 1;
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
    }
  }

  .close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    color: var(--text-light, #FFFFFF);
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .modal-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--gray-medium, #666666);
    text-align: left;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
  }

  .submission-date {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-light, #FFFFFF);
    opacity: 0.7;
  }

  .modal-body {
    padding: 2rem;
    text-align: left;
  }

  .info-section {
    margin-bottom: 2rem;
  }

  .info-section h3 {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
  }

  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
  }

  .info-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--text-light, #FFFFFF);
  }

  .info-item :global(svg) {
    color: #C8102E;
  }

  .label {
    font-weight: 500;
    margin-right: 0.5rem;
  }

  .grievance-type {
    margin-bottom: 1.5rem;
  }

  .description h4 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
  }

  .description p {
    margin: 0;
    line-height: 1.6;
    color: var(--text-light, #FFFFFF);
    opacity: 0.9;
  }

  .description, .redress {
    margin-bottom: 1.5rem;
  }

  .description h4, .redress h4 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
  }

  .description p, .redress p {
    margin: 0;
    line-height: 1.6;
    color: var(--text-light, #FFFFFF);
    opacity: 0.9;
    white-space: pre-line;
  }

  .divider {
    border: none;
    border-top: 1px solid var(--gray-medium, #666666);
    margin: 1.5rem 0;
  }

  @media (max-width: 640px) {
    .modal-content {
      max-height: 100vh;
      border-radius: 0;
    }

    .info-grid {
      grid-template-columns: 1fr;
    }

    .modal-header, .modal-body {
      padding: 1rem;
    }
  }
</style> 