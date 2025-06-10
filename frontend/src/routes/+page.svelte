<script lang="ts">
  import LoginForm from '$lib/components/loginForm/LoginForm.svelte';

  // Assume error is coming in as a prop or from a load function.
  export let error: string | null = null;

  function parseError(error: string): string {
    if (error === 'invalid token') {
      return 'Your token is invalid or expired. Please try again.';
    }
    return 'Something went wrong. Please try again later.';
  }
</script>

<!-- TODO: You should probably have a global +layout file for some reasons: 1. global css. 2. Your <Background> component, since it's used across your entire app. 3. Common css variables in :root {} 4. POSSIBLY also for a single <main> component and styles, given that the app is pretty lean. For reference: https://svelte.dev/docs/kit/routing#layout -->

<h1>Astroulette</h1>
<h2>Random connections across the cosmos</h2>
<!-- Pass the parsed error to the LoginForm -->
<LoginForm error={error ? parseError(error) : null} />

<style>
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
    color: #ecc6a2;
    font-size: clamp(14px, 2vw, 26px);
  }
</style>
