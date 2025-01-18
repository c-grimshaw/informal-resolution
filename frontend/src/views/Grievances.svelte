<script>
  import { store } from '../lib/stores/store.svelte';
  import { post } from '../lib/api/client';
  import { auth } from '../lib/stores/authStore.svelte';

  let formEl = $state(null);
  let submitting = $state(false);
  let step = $state(1);

  const formData = $state({
    submitter_name: '',
    service_number: '',
    rank: '',
    email: '',
    phone: '',
    unit: '',
    position: '',
    grievance_type: '',
    grievance_subtype: '',
    description: '',
    redress_sought: '',
    status: 'pending'
  });

  const grievanceSubTypes = {
    workplace: ['Health and Safety', 'Working Hours', 'Equipment', 'Work Environment'],
    discrimination: ['Age', 'Gender', 'Race', 'Religion', 'Disability', 'Sexual Orientation'],
    harassment: ['Verbal', 'Physical', 'Sexual', 'Psychological', 'Cyber'],
    other: ['Policy Related', 'Administrative', 'Compensation', 'Other']
  };

  const ranks = [
    { value: "Pte(U)", label: "Sailor 3rd Class / Private / Aviator" },
    { value: "Pte(T)", label: "Sailor 2nd Class / Private (Trained) / Aviator (Trained)" },
    { value: "Cpl", label: "Sailor 1st Class / Corporal" },
    { value: "MCpl", label: "Master Sailor / Master Corporal" },
    { value: "Sgt", label: "Petty Officer 2nd Class / Sergeant" },
    { value: "WO", label: "Petty Officer 1st Class / Warrant Officer" },
    { value: "MWO", label: "Master Warrant Officer / Chief Petty Officer 2nd Class" },
    { value: "CWO", label: "Chief Warrant Officer / Chief Petty Officer 1st Class" },
    { value: "OCdt", label: "Officer Cadet / Naval Cadet" },
    { value: "2Lt", label: "Second Lieutenant / Acting Sub-Lieutenant" },
    { value: "Lt", label: "Lieutenant / Sub-Lieutenant" },
    { value: "Capt", label: "Captain / Lieutenant (Navy)" },
    { value: "Maj", label: "Major / Lieutenant-Commander" },
    { value: "LCol", label: "Lieutenant-Colonel / Commander"},
    { value: "Col", label: "Colonel / Captain (Navy)" },
  ];

  function isStepValid(stepNum) {
    switch(stepNum) {
      case 1:
        return formData.submitter_name?.trim() &&
               formData.service_number?.trim() &&
               formData.rank?.trim() &&
               formData.email?.trim() &&
               formData.phone?.trim();
      case 2:
        return formData.unit?.trim() &&
               formData.position?.trim();
      case 3:
        return formData.grievance_type?.trim() &&
               formData.grievance_subtype?.trim() &&
               formData.description?.trim() &&
               formData.redress_sought?.trim();
      default:
        return false;
    }
  }

  function isFormValid() {
    return isStepValid(1) && isStepValid(2) && isStepValid(3);
  }

  async function submitForm(e) {
    e.preventDefault();
    if (!isFormValid()) return;
    
    submitting = true;
    try {
      const title = `${formData.grievance_type} - ${formData.grievance_subtype}`;
      
      const response = await post('/grievances', {
        ...formData,
        title,
        grievance_type: formData.grievance_type,
        grievance_subtype: formData.grievance_subtype,
        submitter_name: formData.submitter_name
      });
      
      store.addGrievance(response);
      resetForm();
      store.setError('✓ Grievance submitted successfully');
    } catch (error) {
      store.setError('Failed to submit grievance: ' + error.message);
    } finally {
      submitting = false;
    }
  }

  function formatDescription() {
    return `
Submitted by: ${formData.submitter_name}
Service Number: ${formData.service_number}
Rank: ${formData.rank}
Contact: ${formData.email} / ${formData.phone}
Position: ${formData.position}
Type: ${formData.grievance_type} - ${formData.grievance_subtype}

Details:
${formData.description}
    `.trim();
  }

  function canSubmitGrievance() {
    return auth.isAuthenticated;
  }

  function resetForm() {
    formData.submitter_name = '';
    formData.service_number = '';
    formData.rank = '';
    formData.email = '';
    formData.phone = '';
    formData.unit = '';
    formData.position = '';
    formData.grievance_type = '';
    formData.grievance_subtype = '';
    formData.description = '';
    formData.redress_sought = '';
    step = 1;
  }
</script>

{#if !canSubmitGrievance()}
  <div class="unauthorized-message">
    <p>You must be logged in to submit grievances.</p>
  </div>
{:else}
  <div class="container">
    <div class="progress-sidebar">
      <div class="progress-step" 
           class:active={step === 1}
           onclick={() => step = 1}
           role="button">
        <div class="step-circle" role="presentation"></div>
        <span>Personal Information</span>
      </div>
      <div class="progress-step" 
           class:active={step === 2}
           onclick={() => step = 2}
           role="button">
        <div class="step-circle" role="presentation"></div>
        <span>Unit Details</span>
      </div>
      <div class="progress-step" 
           class:active={step === 3}
           onclick={() => step = 3}
           role="button">
        <div class="step-circle" role="presentation"></div>
        <span>Grievance Details</span>
      </div>
    </div>

    <div class="form-container">
      <form bind:this={formEl} onsubmit={submitForm}>
        {#if step === 1}
          <div class="form-header">
            <h2>Personal Information</h2>
          </div>
          <div class="form-group">
            <label>Full Name</label>
            <div class="field-description">Enter your legal full name as it appears in official documents</div>
            <input type="text" bind:value={formData.submitter_name} required>
          </div>
          <div class="form-group">
            <label>Service Number</label>
            <div class="field-description">Enter your military service number</div>
            <input type="text" bind:value={formData.service_number} required>
          </div>
          <div class="form-group">
            <label>Rank</label>
            <div class="field-description">Select your current rank</div>
            <select bind:value={formData.rank} required>
              <option value="">Select Rank</option>
              {#each ranks as rank}
                <option value={rank.value}>{rank.label}</option>
              {/each}
            </select>
          </div>
          <div class="form-group">
            <label>Email</label>
            <div class="field-description">Provide your primary JSIS email address</div>
            <input type="email" bind:value={formData.email} placeholder="bloggins.b@sof.cmil.ca" required>
          </div>
          <div class="form-group">
            <label>Phone</label>
            <div class="field-description">Include area code and any extension if applicable</div>
            <input type="tel" bind:value={formData.phone} required>
          </div>
        {/if}

        {#if step === 2}
          <div class="form-header">
            <h2>Unit Details</h2>
          </div>
          <div class="form-group">
            <label>Unit</label>
            <div class="field-description">Select your current assigned unit</div>
            <select bind:value={formData.unit} required>
              <option value="">Select Unit</option>
              <option value="JTF-2">JTF 2</option>
              <option value="CJIRU">CJIRU</option>
              <option value="CSOR">CSOR</option>
              <option value="427SOA">427 SOA</option>
              <option value="CSOTC">CSOTC</option>
              <option value="HQ">HQ</option>
            </select>
          </div>
          <div class="form-group">
            <label>Position/Role</label>
            <div class="field-description">Your current position title / role within the unit</div>
            <input type="text" bind:value={formData.position} required>
          </div>
        {/if}

        {#if step === 3}
          <div class="form-header">
            <h2>Grievance Details</h2>
          </div>
          <div class="form-group">
            <label>Grievance Type</label>
            <div class="field-description">Select the primary category that best describes your grievance</div>
            <select bind:value={formData.grievance_type} required>
              <option value="">Select Type</option>
              <option value="workplace">Workplace Conditions</option>
              <option value="discrimination">Discrimination</option>
              <option value="harassment">Harassment</option>
              <option value="other">Other</option>
            </select>
          </div>
          {#if formData.grievance_type}
            <div class="form-group">
              <label>Grievance Sub-Type</label>
              <div class="field-description">Select a more specific category for your grievance</div>
              <select bind:value={formData.grievance_subtype} required>
                <option value="">Select Sub-Type</option>
                {#each grievanceSubTypes[formData.grievance_type] as subType}
                  <option value={subType}>{subType}</option>
                {/each}
              </select>
            </div>
          {/if}
          <div class="form-group">
            <label>Description</label>
            <div class="field-description">Provide a detailed description of your grievance, including relevant dates, locations, and persons involved</div>
            <textarea bind:value={formData.description} required></textarea>
          </div>
          <div class="form-group">
            <label>Redress Sought</label>
            <div class="field-description">Describe what outcome or resolution you are seeking to resolve this grievance</div>
            <textarea 
              bind:value={formData.redress_sought} 
              required
              placeholder="Explain what actions or changes would resolve this grievance to your satisfaction..."
            ></textarea>
          </div>
        {/if}

        <div class="button-group">
          {#if step > 1}
            <button type="button" onclick={() => step--}>
              Previous
            </button>
          {/if}
          
          {#if step < 3}
            <button type="button" onclick={() => step++} class="next">
              Next
            </button>
          {/if}
          
          {#if step === 3}
            <button type="submit" disabled={submitting || !isFormValid()}>
              {#if submitting}
                <span>Submitting...</span>
              {:else}
                <span>Submit Grievance</span>
              {/if}
            </button>
          {/if}
        </div>
      </form>
    </div>
  </div>
{/if}

<style>
  .container {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 20px;
    width: 100%;
    margin: 0;
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    border: 1px solid var(--gray-medium, #666666);
    overflow: hidden;
    min-height: calc(100vh - 250px);
  }

  .progress-sidebar {
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    padding: 20px;
    border-right: 1px solid var(--gray-medium, #666666);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 20px;
    min-width: 200px;
  }

  .progress-step {
    display: flex;
    align-items: center;
    padding: 15px 10px;
    margin: 10px 0;
    border-radius: 4px;
    transition: all 0.3s;
    font-weight: 300;
    cursor: pointer;
  }

  .progress-step:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .step-circle {
    min-width: 20px;
    min-height: 20px;
    aspect-ratio: 1;
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 50%;
    margin-right: 10px;
    transition: all 0.3s;
  }

  .progress-step.active .step-circle {
    background: var(--primary-red, #C41E3A);
    border-color: var(--primary-red, #C41E3A);
  }

  .progress-step.active {
    background: rgba(196, 30, 58, 0.1);
    font-weight: 400;
  }

  .form-container {
    padding: 30px;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }

  .form-header {
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--text-light, #FFFFFF);
  }

  .form-header h2 {
    color: var(--text-light, #FFFFFF);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 300;
    margin: 0;
  }

  .form-group {
    margin-bottom: 25px;
  }

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 400;
    color: var(--text-light, #FFFFFF);
    text-transform: uppercase;
    font-size: 0.8em;
    letter-spacing: 1px;
  }

  .field-description {
    font-size: 0.8em;
    color: var(--text-light, #FFFFFF);
    opacity: 0.8;
    margin-bottom: 8px;
    font-weight: 300;
  }

  input, select, textarea {
    width: 100%;
    padding: 12px;
    background: var(--primary-dark, #1A1A1A);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 16px;
    color: var(--text-light, #FFFFFF);
    transition: all 0.3s;
    font-family: inherit;
    font-weight: 300;
  }

  input:focus, select:focus, textarea:focus {
    outline: 2px solid white;
    outline-offset: 2px;
    border-color: var(--text-light, #FFFFFF);
  }

  select option {
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
  }

  textarea {
    min-height: 120px;
    resize: vertical;
    line-height: 1.6;
  }

  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
  }

  button {
    min-height: 44px;
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 400;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 16px;
    font-family: inherit;
  }

  button[type="button"] {
    background: var(--primary-dark, #1A1A1A);
    color: var(--text-light, #FFFFFF);
    border: 1px solid var(--gray-medium, #666666);
  }

  button[type="button"]:hover {
    background: var(--gray-medium, #666666);
    border-color: var(--gray-medium, #666666);
  }

  button[type="submit"],
  button.next {
    background: var(--primary-red, #C41E3A);
    color: var(--text-light, #FFFFFF);
    min-width: 150px;
  }

  button[type="submit"]:hover,
  button.next:hover {
    background: #A01830;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background: var(--gray-medium, #666666);
  }

  @media (max-width: 768px) {
    .container {
      grid-template-columns: 1fr;
      margin: 0;
      gap: 0;
      min-height: calc(100vh - 200px);
    }

    .progress-sidebar {
      padding: 10px;
      border-right: none;
      border-bottom: 1px solid var(--gray-medium, #666666);
      flex-direction: row;
      overflow-x: auto;
      min-width: 0;
    }

    .form-container {
      padding: 15px;
      max-width: 100%;
    }

    .button-group {
      flex-direction: column;
      gap: 10px;
    }

    button {
      width: 100%;
    }
  }

  .unauthorized-message {
    text-align: center;
    padding: 2rem;
    background: var(--primary-dark, #1A1A1A);
    border-radius: 8px;
    margin: 1rem;
  }

  .success {
    background: #2e3b2e;
    border: 1px solid #4CAF50;
    color: #4CAF50;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    animation: slideIn 0.3s ease-out;
  }

  .success button {
    background: #4CAF50;
    color: #1a1a1a;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .success button:hover {
    background: #45a049;
  }

  @keyframes slideIn {
    from {
      transform: translateY(-20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>