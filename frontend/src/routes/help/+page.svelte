<script>
  import { AlertCircle, Timer, CheckCircle2 } from "lucide-svelte";
</script>

<div class="help-view">
  <section class="about">
    <h1>About the Informal Resolution Module</h1>
    <p>
      The Informal Resolution Module (IRM) is a digital platform designed to
      streamline the initial grievance process within Canadian Special
      Operations Forces Command (CANSOFCOM). It provides a structured way to
      track, manage, and resolve concerns at the unit level before they escalate
      to formal grievances.
    </p>

    <div class="disclaimer">
      <AlertCircle size={20} />
      <p>
        <strong>Important:</strong> This system does not replace the formal grievance
        process. While the IRM facilitates early resolution of concerns, members
        retain their right to submit formal grievances through official military
        channels. Time spent in informal resolution does not affect formal grievance
        submission deadlines.
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
        <p>Initial submission awaiting review. During this stage:</p>
        <ul>
          <li>Chain of command is notified</li>
          <li>Initial assessment is conducted</li>
          <li>Additional information may be requested</li>
        </ul>
      </div>

      <div class="status-card in-progress">
        <div class="status-header">
          <Timer size={20} />
          <h3>In Progress</h3>
        </div>
        <p>Active informal resolution phase. Actions include:</p>
        <ul>
          <li>Regular communication between parties</li>
          <li>Documentation of resolution attempts</li>
          <li>Exploration of possible solutions</li>
        </ul>
      </div>

      <div class="status-card resolved">
        <div class="status-header">
          <CheckCircle2 size={20} />
          <h3>Resolved</h3>
        </div>
        <p>Concern addressed through informal channels. Outcomes include:</p>
        <ul>
          <li>Agreement on resolution reached</li>
          <li>Documentation of final outcome</li>
          <li>Option to proceed to formal process if needed</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="process">
    <h2>Resolution Process</h2>
    <ol>
      <li>
        <strong>Initial Submission</strong>
        <p>
          Provide detailed information about your concern, including specific
          incidents, dates, and desired outcome.
        </p>
      </li>
      <li>
        <strong>Review and Assessment</strong>
        <p>
          Your chain of command will review the submission and determine the
          appropriate course of action.
        </p>
      </li>
      <li>
        <strong>Informal Resolution</strong>
        <p>
          Work collaboratively with your chain of command to address the concern
          through discussion, mediation, or other appropriate means.
        </p>
      </li>
      <li>
        <strong>Documentation</strong>
        <p>
          All communications and resolution attempts are documented within the
          system for transparency and record-keeping.
        </p>
      </li>
      <li>
        <strong>Outcome</strong>
        <p>
          If resolved informally, the concern is closed. If unresolved, you may
          proceed with the formal grievance process while maintaining a complete
          record of informal resolution attempts.
        </p>
      </li>
    </ol>
  </section>

  <section class="guidelines">
    <h2>Best Practices</h2>
    <div class="guidelines-content">
      <ul>
        <li>Be clear and specific when describing your concern</li>
        <li>Maintain professional communication throughout the process</li>
        <li>Respond promptly to requests for information</li>
        <li>Keep notes of any relevant conversations or events</li>
        <li>Consider reasonable solutions that could resolve the issue</li>
        <li>Respect confidentiality of all parties involved</li>
      </ul>
    </div>
  </section>
</div>

<style>
  .help-view {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
    color: var(--text-light, #ffffff);
  }

  section {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--text-light, #ffffff);
    margin-bottom: 1.5rem;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text-light, #ffffff);
    margin-bottom: 1rem;
  }

  h3 {
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-light, #ffffff);
    margin: 0;
  }

  .disclaimer {
    background: rgba(244, 67, 54, 0.1);
    border: 1px solid #f44336;
    border-radius: 8px;
    padding: 1rem;
    margin: 1.5rem 0;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  .disclaimer :global(svg) {
    color: #f44336;
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
    color: #ffa500;
  }

  .in-progress .status-header :global(svg) {
    color: #64b5f6;
  }

  .resolved .status-header :global(svg) {
    color: #4caf50;
  }

  .pending {
    background: linear-gradient(
        rgba(255, 165, 0, 0.05),
        rgba(255, 165, 0, 0.05)
      ),
      var(--gray-dark, #333333);
  }

  .in-progress {
    background: linear-gradient(
        rgba(100, 181, 246, 0.05),
        rgba(100, 181, 246, 0.05)
      ),
      var(--gray-dark, #333333);
  }

  .resolved {
    background: linear-gradient(
        rgba(76, 175, 80, 0.05),
        rgba(76, 175, 80, 0.05)
      ),
      var(--gray-dark, #333333);
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

  .status-card ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-top: 0.5rem;
  }

  .status-card li {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }

  .process ol {
    counter-reset: process-counter;
    list-style: none;
    padding: 1.5rem;
  }

  .process li {
    counter-increment: process-counter;
    position: relative;
    padding-left: 2.5rem;
    margin-bottom: 1.5rem;
  }

  .process li:before {
    content: counter(process-counter);
    position: absolute;
    left: 0;
    top: 0;
    width: 1.75rem;
    height: 1.75rem;
    background: var(--primary, #1976d2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 500;
  }

  .process li strong {
    display: block;
    margin-bottom: 0.5rem;
    color: var(--primary, #1976d2);
  }

  .process li p {
    font-size: 0.9rem;
    margin: 0;
  }

  .guidelines-content {
    background: var(--gray-dark, #333333);
    border-radius: 8px;
    padding: 1.5rem;
  }

  .guidelines-content ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin: 0;
  }

  .guidelines-content li {
    margin-bottom: 0.75rem;
    line-height: 1.4;
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

    .process li {
      padding-left: 2rem;
    }

    .process li:before {
      width: 1.5rem;
      height: 1.5rem;
      font-size: 0.9rem;
    }
  }
</style>
