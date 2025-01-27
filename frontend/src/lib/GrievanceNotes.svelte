<script>
  import { ChevronDown, ChevronUp } from "lucide-svelte";
  import { store } from "$lib/stores/store.svelte";
  import { get, post } from "$lib/api/client";

  let { grievanceId } = $props();
  let isExpanded = $state(true);
  let notes = $state([]);
  let newNote = $state("");
  let submitting = $state(false);

  async function loadNotes() {
    if (!grievanceId) return;
    try {
      const response = await get(`/grievances/${grievanceId}/notes`);
      notes = response;
    } catch (error) {
      store.setError("Failed to load notes: " + error.message);
    }
  }

  async function addNote() {
    if (!newNote.trim()) return;

    try {
      submitting = true;
      const response = await post(`/grievances/${grievanceId}/notes`, {
        content: newNote.trim(),
      });
      notes = [response, ...notes];
      newNote = "";
      isExpanded = true;
    } catch (error) {
      store.setError("Failed to add note: " + error.message);
    } finally {
      submitting = false;
    }
  }

  function formatDate(dateString) {
    if (!dateString) return "";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-CA", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  }

  $effect(() => {
    if (grievanceId) {
      loadNotes();
    }
  });
</script>

<div class="notes-section">
  <button
    class="section-header"
    onclick={() => (isExpanded = !isExpanded)}
    onkeydown={(e) => e.key === "Enter" && (isExpanded = !isExpanded)}
  >
    <h3>Notes</h3>
    {#if isExpanded}
      <ChevronUp size={20} />
    {:else}
      <ChevronDown size={20} />
    {/if}
  </button>

  {#if isExpanded}
    <div class="notes-content">
      <form
        onsubmit={(e) => {
          e.preventDefault();
          addNote();
        }}
        class="note-form"
      >
        <textarea
          bind:value={newNote}
          placeholder="Add a note or update..."
          rows="3"
          disabled={submitting}
        ></textarea>
        <button type="submit" disabled={submitting || !newNote.trim()}>
          Add Note
        </button>
      </form>

      <div class="notes-list">
        {#each notes as note (note.id)}
          <div class="note">
            <div class="note-header">
              <span class="note-author">{note.user_name}</span>
              <span class="note-date">{formatDate(note.created_at)}</span>
            </div>
            <div class="note-content">
              {note.content}
            </div>
          </div>
        {/each}
        {#if notes.length === 0}
          <div class="no-notes">No notes have been added yet.</div>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .notes-section {
    margin-top: 1rem;
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 8px;
    background: var(--gray-dark, #333333);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    background: var(--primary-dark, #1a1a1a);
    cursor: pointer;
    user-select: none;
    border-radius: 8px 8px 0 0;
    width: 100%;
    border: none;
    color: inherit;
    text-align: left;
    transition: background-color 0.2s ease;
  }

  .section-header:hover {
    background: var(--gray-darker, #222222);
  }

  .section-header h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-light, #ffffff);
  }

  .notes-content {
    padding: 1.25rem;
  }

  .note-form {
    margin-bottom: 1.5rem;
  }

  .note-form textarea {
    width: 100%;
    padding: 1rem;
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 8px;
    background: var(--primary-dark, #1a1a1a);
    color: var(--text-light, #ffffff);
    resize: vertical;
    margin-bottom: 0.75rem;
    font-family: inherit;
    line-height: 1.5;
    transition: all 0.2s ease;
  }

  .note-form textarea:focus {
    outline: none;
    border-color: var(--primary-red, #c41e3a);
    box-shadow: 0 0 0 2px rgba(196, 30, 58, 0.2);
  }

  .note-form button {
    padding: 0.75rem 1.5rem;
    background: var(--primary-red, #c41e3a);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .note-form button:hover:not(:disabled) {
    background: #a01830;
    transform: translateY(-1px);
  }

  .note-form button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .notes-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .note {
    background: var(--primary-dark, #1a1a1a);
    border: 1px solid var(--gray-medium, #666666);
    border-radius: 8px;
    padding: 1.25rem;
    transition: all 0.2s ease;
  }

  .note:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .note-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
  }

  .note-author {
    font-weight: 500;
    color: var(--primary-red, #c41e3a);
  }

  .note-date {
    color: var(--gray-light, #999999);
  }

  .note-content {
    white-space: pre-wrap;
    color: var(--text-light, #ffffff);
    line-height: 1.6;
    font-size: 0.95rem;
  }

  .no-notes {
    text-align: center;
    padding: 2rem;
    color: var(--gray-light, #999999);
    font-style: italic;
    background: var(--primary-dark, #1a1a1a);
    border-radius: 8px;
    border: 1px dashed var(--gray-medium, #666666);
  }

  @media (max-width: 640px) {
    .section-header {
      padding: 0.75rem 1rem;
    }

    .notes-content {
      padding: 1rem;
    }

    .note {
      padding: 1rem;
    }
  }
</style>

