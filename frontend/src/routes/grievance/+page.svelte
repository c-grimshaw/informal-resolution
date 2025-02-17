<script>
  import { store } from "$lib/stores/store.svelte";
  import { post } from "$lib/api/client";
  import { auth } from "$lib/stores/authStore.svelte";
  import { onMount } from "svelte";
  import { ranks, units, grievanceTypes } from "$lib/constants";

  let formEl = $state(null);
  let submitting = $state(false);
  let step = $state(1);

  // Initialize formData with saved state or defaults
  const formData = $state(
    loadFormState() || {
      submitter_name: auth.user?.name || "",
      service_number: auth.user?.service_number || "",
      rank: auth.user?.rank || "",
      email: auth.user?.email || "",
      phone: auth.user?.phone || "",
      unit: auth.user?.unit || "",
      position: auth.user?.position || "",
      grievance_type: "",
      grievance_subtype: "",
      description: "",
      redress_sought: "",
      status: "pending",
    },
  );

  // Load saved form state from localStorage
  function loadFormState() {
    try {
      const savedState = localStorage.getItem("grievanceFormState");
      if (savedState) {
        const parsedState = JSON.parse(savedState);
        // Also restore the step if it was saved
        const savedStep = localStorage.getItem("grievanceFormStep");
        if (savedStep) {
          step = parseInt(savedStep, 10);
        }
        return parsedState;
      }
    } catch (error) {
      console.error("Error loading form state:", error);
    }
    return null;
  }

  // Save form state to localStorage
  function saveFormState() {
    try {
      localStorage.setItem("grievanceFormState", JSON.stringify(formData));
      localStorage.setItem("grievanceFormStep", step.toString());
    } catch (error) {
      console.error("Error saving form state:", error);
    }
  }

  // Clear saved form state
  function clearFormState() {
    try {
      localStorage.removeItem("grievanceFormState");
      localStorage.removeItem("grievanceFormStep");
    } catch (error) {
      console.error("Error clearing form state:", error);
    }
  }

  // Watch for changes in formData and step
  $effect(() => {
    if (canSubmitGrievance()) {
      saveFormState();
    }
  });

  $effect(() => {
    if (auth.user) {
      formData.submitter_name = auth.user.name || formData.submitter_name;
      formData.service_number =
        auth.user.service_number || formData.service_number;
      formData.rank = auth.user.rank || formData.rank;
      formData.email = auth.user.email || formData.email;
      formData.phone = auth.user.phone || formData.phone;
      formData.unit = auth.user.unit || formData.unit;
      formData.position = auth.user.position || formData.position;
    }
  });

  function isStepValid(stepNum) {
    switch (stepNum) {
      case 1:
        return (
          formData.submitter_name?.trim() &&
          formData.service_number?.trim() &&
          formData.rank?.trim() &&
          formData.email?.trim() &&
          formData.phone?.trim()
        );
      case 2:
        return formData.unit?.trim() && formData.position?.trim();
      case 3:
        return (
          formData.grievance_type?.trim() &&
          formData.grievance_subtype?.trim() &&
          formData.description?.trim() &&
          formData.redress_sought?.trim()
        );
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

      const response = await post("/grievances", {
        ...formData,
        title,
        grievance_type: formData.grievance_type,
        grievance_subtype: formData.grievance_subtype,
        submitter_name: formData.submitter_name,
      });

      store.addGrievance(response);
      resetForm(); // This will also clear the saved state
      store.setError("✓ Grievance submitted successfully");
    } catch (error) {
      store.setError("Failed to submit grievance: " + error.message);
    } finally {
      submitting = false;
    }
  }

  function canSubmitGrievance() {
    return auth.isAuthenticated;
  }

  // Reset form and clear saved state
  function resetForm() {
    formData.submitter_name = "";
    formData.service_number = "";
    formData.rank = "";
    formData.email = "";
    formData.phone = "";
    formData.unit = "";
    formData.position = "";
    formData.grievance_type = "";
    formData.grievance_subtype = "";
    formData.description = "";
    formData.redress_sought = "";
    step = 1;
    clearFormState();
  }

  // Add cleanup on component unmount
  onMount(() => {
    return () => {
      if (!isFormValid()) {
        saveFormState(); // Save state when navigating away if form is incomplete
      }
    };
  });
</script>

{#if !canSubmitGrievance()}
  <div class="unauthorized-message">
    <p>You must be logged in to submit grievances.</p>
  </div>
{:else}
  <div class="container">
    <div class="progress-sidebar">
      <div
        class="progress-step"
        class:active={step === 1}
        onclick={() => (step = 1)}
        role="button"
        tabindex="0"
      >
        <div class="step-circle" role="presentation"></div>
        <span>Personal Information</span>
      </div>
      <div
        class="progress-step"
        class:active={step === 2}
        onclick={() => (step = 2)}
        role="button"
        tabindex="0"
      >
        <div class="step-circle" role="presentation"></div>
        <span>Unit Details</span>
      </div>
      <div
        class="progress-step"
        class:active={step === 3}
        onclick={() => (step = 3)}
        role="button"
        tabindex="0"
      >
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
            <label for="submitter_name">Full Name</label>
            <div class="field-description">
              Enter your legal full name as it appears in official documents
            </div>
            <input
              type="text"
              id="submitter_name"
              bind:value={formData.submitter_name}
              required
            />
          </div>
          <div class="form-group">
            <label for="service_number">Service Number</label>
            <div class="field-description">
              Enter your military service number
            </div>
            <input
              type="text"
              id="service_number"
              bind:value={formData.service_number}
              required
            />
          </div>
          <div class="form-group">
            <label for="rank">Rank</label>
            <div class="field-description">Select your current rank</div>
            <select id="rank" bind:value={formData.rank} required>
              <option value="">Select Rank</option>
              {#each ranks as rank}
                <option value={rank.value}>{rank.label}</option>
              {/each}
            </select>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <div class="field-description">
              Provide your primary JSIS email address
            </div>
            <input
              type="email"
              id="email"
              bind:value={formData.email}
              placeholder="bloggins.b@sof.cmil.ca"
              required
            />
          </div>
          <div class="form-group">
            <label for="phone">Phone</label>
            <div class="field-description">
              Include area code and any extension if applicable
            </div>
            <input type="tel" id="phone" bind:value={formData.phone} required />
          </div>
        {/if}

        {#if step === 2}
          <div class="form-header">
            <h2>Unit Details</h2>
          </div>
          <div class="form-group">
            <label for="unit">Unit</label>
            <div class="field-description">
              Select your current assigned unit
            </div>
            <select id="unit" bind:value={formData.unit} required>
              <option value="">Select Unit</option>
              {#each units as unit}
                <option value={unit.value}>{unit.label}</option>
              {/each}
            </select>
          </div>
          <div class="form-group">
            <label for="position">Position/Role</label>
            <div class="field-description">
              Your current position title / role within the unit
            </div>
            <input
              type="text"
              id="position"
              bind:value={formData.position}
              required
            />
          </div>
        {/if}

        {#if step === 3}
          <div class="form-header">
            <h2>Grievance Details</h2>
          </div>
          <div class="form-group">
            <label for="grievance_type">Grievance Type</label>
            <div class="field-description">
              Select the primary category that best describes your grievance
            </div>
            <select
              id="grievance_type"
              bind:value={formData.grievance_type}
              required
            >
              <option value="">Select Type</option>
              {#each grievanceTypes as type}
                <option value={type.value}>{type.label}</option>
              {/each}
            </select>
          </div>
          {#if formData.grievance_type}
            <div class="form-group">
              <label for="grievance_subtype">Grievance Sub-Type</label>
              <div class="field-description">
                Select a more specific category for your grievance
              </div>
              <select
                id="grievance_subtype"
                bind:value={formData.grievance_subtype}
                required
              >
                <option value="">Select Sub-Type</option>
                {#each grievanceTypes.find((t) => t.value === formData.grievance_type).subtypes as subType}
                  <option value={subType}>{subType}</option>
                {/each}
              </select>
            </div>
          {/if}
          <div class="form-group">
            <label for="description">Description</label>
            <div class="field-description">
              Provide a detailed description of your grievance, including
              relevant dates, locations, and persons involved
            </div>
            <textarea
              id="description"
              bind:value={formData.description}
              required
            ></textarea>
          </div>
          <div class="form-group">
            <label for="redress_sought">Redress Sought</label>
            <div class="field-description">
              Describe what outcome or resolution you are seeking to resolve
              this grievance
            </div>
            <textarea
              id="redress_sought"
              bind:value={formData.redress_sought}
              required
            ></textarea>
          </div>
        {/if}

        <div class="button-group">
          {#if step > 1}
            <button type="button" onclick={() => step--}> Previous </button>
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
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--gray-medium, #666666);
    overflow: hidden;
    min-height: calc(100vh - 250px);
  }

  .progress-sidebar {
    background: var(--primary-dark, #1a1a1a);
    color: var(--text-light, #ffffff);
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
    background: var(--primary-red, #c41e3a);
    border-color: var(--primary-red, #c41e3a);
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
    border-bottom: 1px solid var(--text-light, #ffffff);
  }

  .form-header h2 {
    color: var(--text-light, #ffffff);
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
    color: var(--text-light, #ffffff);
    text-transform: uppercase;
    font-size: 0.8em;
    letter-spacing: 1px;
  }

  .field-description {
    font-size: 0.8em;
    color: var(--text-light, #ffffff);
    opacity: 0.8;
    margin-bottom: 8px;
    font-weight: 300;
  }

  input,
  select,
  textarea {
    width: 100%;
    padding: 12px;
    background: var(--primary-dark, #1a1a1a);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 16px;
    color: var(--text-light, #ffffff);
    transition: all 0.3s;
    font-family: inherit;
    font-weight: 300;
  }

  input:focus,
  select:focus,
  textarea:focus {
    outline: 2px solid white;
    outline-offset: 2px;
    border-color: var(--text-light, #ffffff);
  }

  select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 16px;
    padding-right: 40px;
  }

  select:focus {
    outline: 2px solid var(--primary-red, #c41e3a);
    outline-offset: 0;
    border-color: var(--primary-red, #c41e3a);
  }

  select option {
    padding: 12px;
    background: var(--primary-dark, #1a1a1a);
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
    background: var(--primary-dark, #1a1a1a);
    color: var(--text-light, #ffffff);
    border: 1px solid var(--gray-medium, #666666);
  }

  button[type="button"]:hover {
    background: var(--gray-medium, #666666);
    border-color: var(--gray-medium, #666666);
  }

  button[type="submit"],
  button.next {
    background: var(--primary-red, #c41e3a);
    color: var(--text-light, #ffffff);
    min-width: 150px;
  }

  button[type="submit"]:hover,
  button.next:hover {
    background: #a01830;
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
    background: var(--primary-dark, #1a1a1a);
    border-radius: 8px;
    margin: 1rem;
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
