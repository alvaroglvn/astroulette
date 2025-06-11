<script lang="ts">
  export let error: string | null = null;
  export let success: boolean = false;
  let submitting = false;
</script>

<div class="login-form">
  <h3>Begin interplanetary relay</h3>

  <form
    method="POST"
    on:submit={() => {
      submitting = true;
    }}
  >
    {#if error}
      <p class="form-response error">
        {error}
      </p>
    {/if}

    <input
      name="username"
      type="text"
      placeholder="Your username"
      autocomplete="username"
      required
    />

    <input
      name="email"
      type="email"
      placeholder="Your email"
      autocomplete="email"
      required
    />

    <button type="submit" disabled={submitting}
      >{submitting ? 'Submitting...' : `Let's go!`}</button
    >

    {#if success}
      <p class="success-msg">Check your email for your login link</p>
    {/if}
  </form>
</div>

<style>
  .login-form {
    width: 65vw;
    max-width: 550px;
    font-family: var(--font-display);
  }
  h3 {
    font-size: clamp(14px, 4vw, 34px);
    color: var(--pink-500);
    text-transform: uppercase;
    text-align: center;
    margin: 0;
    line-height: 0.73em;
  }
  form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 2em;
    background-color: #2e4770;
    border: 9px double var(--pink-500);
  }
  form input {
    font-size: 16px;
    padding: 0.5em;
  }
  form button {
    padding: 0.25em;
    background-color: var(--soft-yellow);
    font-family: var(--font-display);
    font-size: x-large;
    font-weight: bold;
    cursor: pointer;
    border: none;
    transition: background 0.2s;
  }
  form button:hover:enabled {
    background-color: var(--button-hover, #eca089);
  }
  form button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  .form-response.error {
    text-align: center;
    color: var(--pink-500);
    font-size: clamp(1.8rem, 2.5vw, 2rem);
  }
  .success-msg {
    text-align: center;
    color: var(--soft-yellow);
    font-size: clamp(1.8rem, 2.5vw, 2rem);
    line-height: clamp(0.5rem, 5vw, 2rem);
    font-family: var(--font-display);
  }
  @media (max-width: 768px) {
    form button {
      font-size: 14px;
    }
    form input {
      font-size: 12px;
    }
  }
</style>
