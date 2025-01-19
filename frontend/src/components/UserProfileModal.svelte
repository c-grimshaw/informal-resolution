<script>
  import { 
    User, 
    Building2, 
    Phone,
    Mail,
    Medal,
    Hash,
    X
  } from 'lucide-svelte';
  import { auth } from '../lib/stores/authStore.svelte';
  import { store } from '../lib/stores/store.svelte';
  import { patch } from '../lib/api/client';
  import { ranks, units } from '../lib/constants';

  let { isOpen = false, closeModal = $bindable(), onProfileUpdate = $bindable() } = $props();
  
  let submitting = $state(false);
  let formData = $state({
    name: auth.user?.name || '',
    service_number: auth.user?.service_number || '',
    rank: auth.user?.rank || '',
    email: auth.user?.email || '',
    phone: auth.user?.phone || '',
    unit: auth.user?.unit || '',
    position: auth.user?.position || ''
  });

  // Update formData when auth.user changes
  $effect(() => {
    if (auth.user) {
      formData = {
        name: auth.user.name || '',
        service_number: auth.user.service_number || '',
        rank: auth.user.rank || '',
        email: auth.user.email || '',
        phone: auth.user.phone || '',
        unit: auth.user.unit || '',
        position: auth.user.position || ''
      };
    }
  });

  async function handleSubmit(e) {
    e.preventDefault();
    submitting = true;
    
    try {
      // Remove email from the update payload since it can't be changed
      const { email, ...updateData } = formData;
      
      const response = await patch(`/users/me`, updateData);
      auth.setUser(response);
      store.setError('✓ Profile updated successfully');
      if (onProfileUpdate) onProfileUpdate();
      closeModal();
    } catch (error) {
      store.setError('Failed to update profile: ' + error.message);
    } finally {
      submitting = false;
    }
  }

  function handleBackdropClick(event) {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }
</script>

{#if isOpen}
  <div class="modal-backdrop" 
    role="button"
    tabindex="0"
    onclick={handleBackdropClick}
    onkeydown={(e) => e.key === 'Escape' && closeModal()}
  >
    <div class="modal-content" 
      onclick={(e) => e.stopPropagation()}
    >
      <button class="close-button" onclick={closeModal}>
        <X size={24} />
      </button>

      <div class="modal-header">
        <h2>Edit Profile</h2>
      </div>

      <form class="modal-body" onsubmit={handleSubmit}>
        <div class="form-group">
          <label for="name">
            <User size={16} />
            Full Name
          </label>
          <div class="field-description">Your legal full name as it appears in official documents</div>
          <input type="text" id="name" bind:value={formData.name} required>
        </div>

        <div class="form-group">
          <label for="service_number">
            <Hash size={16} />
            Service Number
          </label>
          <div class="field-description">Your military service number</div>
          <input type="text" id="service_number" bind:value={formData.service_number} required>
        </div>

        <div class="form-group">
          <label for="rank">
            <Medal size={16} />
            Rank
          </label>
          <div class="field-description">Your current rank</div>
          <select id="rank" bind:value={formData.rank} required>
            <option value="">Select Rank</option>
            {#each ranks as rank}
              <option value={rank.value}>{rank.label}</option>
            {/each}
          </select>
        </div>

        <div class="form-group">
          <label for="email">
            <Mail size={16} />
            Email
          </label>
          <div class="field-description">Your JSIS email address (cannot be changed)</div>
          <input 
            type="email" 
            id="email" 
            value={formData.email} 
            readonly 
            class="readonly"
          >
        </div>

        <div class="form-group">
          <label for="phone">
            <Phone size={16} />
            Phone
          </label>
          <div class="field-description">Include area code and any extension if applicable</div>
          <input type="tel" id="phone" bind:value={formData.phone} required>
        </div>

        <div class="form-group">
          <label for="unit">
            <Building2 size={16} />
            Unit
          </label>
          <div class="field-description">Your current assigned unit</div>
          <select id="unit" bind:value={formData.unit} required>
            <option value="">Select Unit</option>
            {#each units as unit}
              <option value={unit.value}>{unit.label}</option>
            {/each}
          </select>
        </div>

        <div class="form-group">
          <label for="position">
            <User size={16} />
            Position
          </label>
          <div class="field-description">Your current position or role within the unit</div>
          <input type="text" id="position" bind:value={formData.position} required>
        </div>

        <div class="button-group">
          <button type="submit" disabled={submitting}>
            {submitting ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

<style>
  @media (max-width: 640px) {
    .modal-content {
      width: 100%;
      height: 100%;
      max-height: 100vh;
      border-radius: 0;
      border: none;
    }

    .modal-header {
      padding: 1rem;
    }

    .modal-body {
      padding: 1rem;
    }
  }

  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background: var(--primary-dark, #1A1A1A);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  .modal-header {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--gray-medium, #666666);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
  }

  .modal-body {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .close-button {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    background: none;
    border: none;
    color: var(--text-light, #FFFFFF);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 4px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  label {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    color: var(--text-light, #FFFFFF);
    font-weight: 500;
    font-size: 0.875rem;
  }

  .field-description {
    font-size: 0.75rem;
    color: var(--gray-light, #999999);
    margin-bottom: 0.125rem;
  }

  input, select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid var(--gray-medium, #666666);
    background: var(--gray-dark, #333333);
    color: var(--text-light, #FFFFFF);
    font-size: 0.875rem;
    width: 100%;
    transition: all 0.2s;
  }

  input:focus, select:focus {
    outline: none;
    border-color: #C8102E;
    box-shadow: 0 0 0 1px rgba(200, 16, 46, 0.2);
  }

  select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 8px center;
    background-size: 16px;
    padding-right: 32px;
  }

  .button-group {
    margin-top: 1.5rem;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }

  button[type="submit"] {
    background: #C8102E;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  button[type="submit"]:hover {
    background: #E31837;
    transform: translateY(-1px);
  }

  button[type="submit"]:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }

  input.readonly {
    opacity: 0.7;
    cursor: not-allowed;
    background: var(--gray-dark, #333333);
    border-color: var(--gray-medium, #666666);
  }

  input.readonly:focus {
    outline: none;
    border-color: var(--gray-medium, #666666);
    box-shadow: none;
  }
</style>