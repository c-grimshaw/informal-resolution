<script>
  import { AlertCircle, Timer, CheckCircle2 } from 'lucide-svelte';
</script>

<div class="help-view">
  <section class="about">
    <h1>About the Informal Resolution System</h1>
    <p>
      The Informal Resolution System helps track and manage initial grievance communications within military units 
      before entering the formal process.
    </p>
    
    <div class="disclaimer">
      <AlertCircle size={20} />
      <p>
        <strong>Important:</strong> This system does not replace the formal grievance process. 
        You can escalate concerns within this app if informal resolution is unsatisfactory. 
        All formal grievances must still be submitted through official military channels.
      </p>
    </div>
  </section>

  <section class="status-guide">
    <h2>Status Levels</h2>
    <div class="status-cards">
      <div class="status-card pending">
        <div class="status-header">
          <AlertCircle size={20} />
          <h3>Pending</h3>
        </div>
        <p>
          New submission awaiting review by chain of command.
        </p>
      </div>

      <div class="status-card in-progress">
        <div class="status-header">
          <Timer size={20} />
          <h3>In Progress</h3>
        </div>
        <p>
          Being actively reviewed and addressed through informal channels.
        </p>
      </div>

      <div class="status-card resolved">
        <div class="status-header">
          <CheckCircle2 size={20} />
          <h3>Resolved</h3>
        </div>
        <p>
          Issue addressed through informal channels. If unsatisfied, proceed with formal grievance process.
        </p>
      </div>
    </div>
  </section>

  <section class="process">
    <h2>Process</h2>
    <ol>
      <li>Submit concern with details and desired resolution</li>
      <li>Chain of command reviews and addresses the issue</li>
      <li>Work toward informal resolution</li>
      <li>If unresolved, proceed with formal grievance process</li>
    </ol>
  </section>
</div>

<style>
  .help-view {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
    color: var(--text-light, #FFFFFF);
  }

  section {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
    margin-bottom: 1.5rem;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
    margin-bottom: 1rem;
  }

  h3 {
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-light, #FFFFFF);
    margin: 0;
  }

  .disclaimer {
    background: rgba(244, 67, 54, 0.1);
    border: 1px solid #F44336;
    border-radius: 8px;
    padding: 1rem;
    margin: 1.5rem 0;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  .disclaimer :global(svg) {
    color: #F44336;
    flex-shrink: 0;
    margin-top: 0.25rem;
  }

  .status-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
  }

  .status-card {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 1.5rem;
  }

  .status-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .pending .status-header :global(svg) {
    color: #FFA500;
  }

  .in-progress .status-header :global(svg) {
    color: #64B5F6;
  }

  .resolved .status-header :global(svg) {
    color: #4CAF50;
  }

  .pending {
    background: linear-gradient(rgba(255, 165, 0, 0.05), rgba(255, 165, 0, 0.05)), var(--gray-dark, #333333);
  }

  .in-progress {
    background: linear-gradient(rgba(100, 181, 246, 0.05), rgba(100, 181, 246, 0.05)), var(--gray-dark, #333333);
  }

  .resolved {
    background: linear-gradient(rgba(76, 175, 80, 0.05), rgba(76, 175, 80, 0.05)), var(--gray-dark, #333333);
  }

  ol {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 1.5rem 1.5rem 1.5rem 3rem;
    margin: 0;
  }

  li {
    margin-bottom: 1rem;
    line-height: 1.6;
  }

  li:last-child {
    margin-bottom: 0;
  }

  @media (max-width: 768px) {
    .help-view {
      padding: 1rem;
    }

    .status-cards {
      grid-template-columns: 1fr;
    }

    h1 {
      font-size: 1.35rem;
    }

    h2 {
      font-size: 1.15rem;
    }
  }
</style> 