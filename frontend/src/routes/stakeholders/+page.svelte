<script>
  import { store } from "$lib/stores/store.svelte";
  import StakeholdersTable from "$lib/StakeholdersTable.svelte";
</script>

<div class="stakeholders-view">
  <header>
    <h1>Stakeholders</h1>
  </header>

  <StakeholdersTable stakeholders={store.stakeholders} />
</div>

<style>
  .stakeholders-view {
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  header {
    margin-bottom: 1.5rem;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--text-light, #ffffff);
    margin: 0;
  }
</style>
