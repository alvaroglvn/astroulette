<script lang="ts">
  import LoginForm from '$lib/components/loginForm/LoginForm.svelte';

  // export let data: { error?: string | null };
  export let form: { error?: string | null; success?: boolean } | undefined;

  function parseError(error: string): string {
    if (error === 'invalid token') {
      return 'Your token is invalid or expired. Please try again.';
    }
    return 'Something went wrong. Please try again later.';
  }
</script>

<h1>Astroulette</h1>
<h2>Random connections across the cosmos</h2>
<LoginForm
  error={form?.error ? parseError(form.error) : null}
  success={form?.success ?? false}
/>

<style>
  h1,
  h2 {
    font-family: var(--font-display);
  }

  h1 {
    font-style: italic;

    text-transform: uppercase;
    font-size: clamp(42px, 8vw, 90px);
    text-shadow:
      0 0 2px var(--pink-500),
      0 0 10px var(--pink-500);
    margin: 0px;
    padding: 0px;
    line-height: 0px;
  }

  h2 {
    margin-top: 2em;
    margin-bottom: 5em;
    color: var(--soft-yellow);
    font-size: clamp(14px, 2vw, 26px);
  }

  @media (max-width: 768px) {
    h2 {
      margin-top: 0.5em;
    }
  }
</style>
