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
    --soft-yellow: #ecd9c9;
    --main-padding: 5rem 2.5rem;
    --main-gap: 2rem;
    --container-max-width: 600px;
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    padding: var(--main-padding);
    gap: var(--main-gap);
    font-family: var(--font-display);
    max-width: var(--container-max-width);
  }
</style>
