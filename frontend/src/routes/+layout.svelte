<script>
  import Background from '$lib/components/Background.svelte';

  let { children } = $props();
</script>

<svelte:head>
  <title>Astroulette</title>
  <link rel="icon" href="/favicon.ico" type="image/x-icon" />
  <meta charset="UTF-8" />
  <meta
    name="description"
    content="Drift into a retro-futuristic galaxy where you chat with AI-generated alien strangers. Discover weird worlds and unexpected conversations."
  />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <meta property="og:title" content="Astroulette" />
  <meta
    property="og:image"
    content="https://astroulette.fly.dev/og-image.png"
  />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta
    property="og:description"
    content="Drift into a retro-futuristic galaxy where you chat with AI-generated alien strangers. Discover weird worlds and unexpected conversations."
  />
  <meta property="og:url" content="https://astroulette.fly.dev" />
  <meta property="og:type" content="website" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Astroulette" />
  <meta
    name="twitter:description"
    content="Drift into a retro-futuristic galaxy where you chat with AI-generated alien strangers. Discover weird worlds and unexpected conversations."
  />
  <meta
    name="twitter:image"
    content="https://astroulette.fly.dev/og-image.png"
  />
  <meta
    name="twitter:image:alt"
    content="Smiling aliens in a retro synthwave galactic background"
  />
</svelte:head>

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
