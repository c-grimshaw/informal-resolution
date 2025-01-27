<script>
  import { personalGrievances } from "$lib/stores/personalGrievances.svelte.js";
  import GrievanceTable from "$lib/GrievanceTable.svelte";

  function handleGrievanceDelete(grievanceId) {
    personalGrievances.deleteGrievance(grievanceId);
  }

</script>

<div class="home">
  <h1>Informal Resolution Module</h1>

  <div class="grievances-section">
    <h2>My Grievances</h2>
    {#if personalGrievances.loading}
      <div class="loading-state">
        <p>Loading grievances...</p>
      </div>
    {:else if !personalGrievances.grievances?.length}
      <div class="empty-state">
        <p>You have no current grievances in the system.</p>
        <p>
          To submit a new grievance, click the "Grievances" button in the
          navigation bar.
        </p>
      </div>
    {:else}
      <GrievanceTable
        grievances={personalGrievances.grievances}
        showColumns={["grievance_type", "status", "created_at"]}
        canEditStatus={false}
        readonly={true}
        canDelete={true}
        onDelete={handleGrievanceDelete}
        showFilters={false}
      />
    {/if}
  </div>
</div>

<style>
  .home {
    text-align: center;
  }

  h1 {
    margin-bottom: 2rem;
    color: var(--text-light, #ffffff);
  }

  h2 {
    margin: 2rem 0;
    color: var(--text-light, #ffffff);
    text-align: left;
  }

  .grievances-section {
    margin-top: 3rem;
  }

  .empty-state, .loading-state {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    color: var(--text-light, #ffffff);
  }

  .empty-state p, .loading-state p {
    margin: 0.5rem 0;
    line-height: 1.5;
  }

  .empty-state p:first-child {
    font-size: 1.1em;
    font-weight: 500;
  }

  .empty-state p:last-child {
    color: var(--gray-light, #999999);
  }

  .loading-state p {
    font-size: 1.1em;
    font-weight: 500;
    opacity: 0.8;
  }
</style>
