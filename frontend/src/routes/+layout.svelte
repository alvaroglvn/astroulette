<script>
  import Background from '$lib/components/Background.svelte';

  let { children } = $props();
</script>

<main>
  <Background />
  {@render children()}
</main>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');

  :root {
    --font-display: 'Space Grotesk', sans-serif;
    --pink-500: #ce5e82;
  }

  :global(html, body) {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
    font-family: var(--font-display);
    color: var(--pink-500);
  }

  :global(body) {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  :global(*) {
    box-sizing: border-box;
  }

  main {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    padding: 5rem;
    gap: 3rem;
    font-family: 'Space Grotesk', sans-serif;
    height: 100%;
    flex-direction: column;
    gap: 2rem;
    padding: 5rem 2.5rem;
    max-width: 600px;
  }
</style>
