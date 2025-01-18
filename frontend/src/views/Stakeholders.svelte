<script>
  import { onMount } from 'svelte';
  import { stakeholders, loading, error } from '../lib/stores/store';
  import { get, post, put, del } from '../lib/api/client';

  let newStakeholder = {
    name: '',
    email: '',
    role: 'user'
  };

  async function loadStakeholders() {
    try {
      $loading = true;
      const data = await get('/api/stakeholders');
      $stakeholders = data;
    } catch (e) {
      $error = e.message;
    } finally {
      $loading = false;
    }
  }

  async function handleSubmit() {
    try {
      $loading = true;
      const response = await post('/api/stakeholders', newStakeholder);
      $stakeholders = [...$stakeholders, response];
      newStakeholder = { name: '', email: '', role: 'user' };
    } catch (e) {
      $error = e.message;
    } finally {
      $loading = false;
    }
  }

  async function handleRoleChange(stakeholder) {
    try {
      $loading = true;
      const response = await put(`/api/stakeholders/${stakeholder.id}`, stakeholder);
      $stakeholders = $stakeholders.map(s => s.id === stakeholder.id ? response : s);
    } catch (e) {
      $error = e.message;
    } finally {
      $loading = false;
    }
  }

  async function handleDelete(id) {
    if (!confirm('Are you sure you want to delete this stakeholder?')) return;
    
    try {
      $loading = true;
      await del(`/api/stakeholders/${id}`);
      $stakeholders = $stakeholders.filter(s => s.id !== id);
    } catch (e) {
      $error = e.message;
    } finally {
      $loading = false;
    }
  }

  onMount(loadStakeholders);
</script>

<div class="stakeholders">
  <h2>Stakeholders</h2>

  <form on:submit|preventDefault={handleSubmit} class="new-stakeholder-form">
    <input
      type="text"
      bind:value={newStakeholder.name}
      placeholder="Stakeholder Name"
      required
    />
    <input
      type="email"
      bind:value={newStakeholder.email}
      placeholder="Email Address"
      required
    />
    <select bind:value={newStakeholder.role}>
      <option value="user">User</option>
      <option value="admin">Admin</option>
      <option value="manager">Manager</option>
    </select>
    <button type="submit">Add Stakeholder</button>
  </form>

  <div class="stakeholders-list">
    {#each $stakeholders as stakeholder}
      <div class="stakeholder-card">
        <div class="stakeholder-info">
          <h3>{stakeholder.name}</h3>
          <p>{stakeholder.email}</p>
        </div>
        <div class="stakeholder-actions">
          <select
            bind:value={stakeholder.role}
            on:change={() => handleRoleChange(stakeholder)}
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
            <option value="manager">Manager</option>
          </select>
          <button
            class="delete-btn"
            on:click={() => handleDelete(stakeholder.id)}
          >
            Delete
          </button>
        </div>
      </div>
    {:else}
      <p class="no-stakeholders">No stakeholders found.</p>
    {/each}
  </div>
</div>

<style>
  .stakeholders {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  h2 {
    color: var(--text-light, #FFFFFF);
    font-weight: 300;
    font-size: 2rem;
    margin: 0 0 2rem 0;
  }

  .new-stakeholder-form {
    background: var(--gray-dark, #333333);
    padding: 2rem;
    border-radius: 8px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  input, select {
    padding: 0.75rem 1rem;
    background: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    color: var(--text-light, #FFFFFF);
    font-size: 0.95rem;
    transition: border-color 0.2s;
  }

  input:focus, select:focus {
    outline: none;
    border-color: #4a9eff;
  }

  input::placeholder {
    color: #888;
  }

  button {
    padding: 0.75rem 1.5rem;
    background: #4a9eff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    transition: background-color 0.2s, transform 0.1s;
  }

  button:hover {
    background: #3a8eef;
    transform: translateY(-1px);
  }

  button:active {
    transform: translateY(0);
  }

  .stakeholders-list {
    display: grid;
    gap: 1rem;
  }

  .stakeholder-card {
    background: var(--gray-dark, #333333);
    padding: 1.5rem;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s;
  }

  .stakeholder-card:hover {
    transform: translateY(-2px);
  }

  .stakeholder-info h3 {
    margin: 0;
    color: var(--text-light, #FFFFFF);
    font-weight: 500;
    font-size: 1.1rem;
  }

  .stakeholder-info p {
    margin: 0.5rem 0 0;
    color: #888;
    font-size: 0.9rem;
  }

  .stakeholder-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .stakeholder-actions select {
    min-width: 120px;
  }

  .delete-btn {
    background: #ff4a4a;
    padding: 0.6rem 1.2rem;
  }

  .delete-btn:hover {
    background: #ef3a3a;
  }

  .no-stakeholders {
    text-align: center;
    color: #888;
    background: var(--gray-dark, #333333);
    padding: 2rem;
    border-radius: 8px;
    font-size: 1.1rem;
  }

  @media (max-width: 768px) {
    .stakeholders {
      padding: 1rem;
    }

    .new-stakeholder-form {
      padding: 1.5rem;
      grid-template-columns: 1fr;
    }

    .stakeholder-card {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .stakeholder-actions {
      width: 100%;
      justify-content: center;
    }
  }
</style> 