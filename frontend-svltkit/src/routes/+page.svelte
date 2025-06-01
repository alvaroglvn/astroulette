<script lang="ts">
  import Background from '$lib/components/Background.svelte';
  import LoginForm from '$lib/components/LoginForm.svelte';
  export let data;
  export let form;
</script>

<main>
  <Background />
  <h1>Astroulette</h1>
  <h2>Random connections across the cosmos</h2>
  <LoginForm {data} {form} />
</main>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');

  :global(html, body) {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
    font-family: 'Space Grotesk', sans-serif;
    color: #ce5e82;
  }

  :global(body) {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  :global(*) {
    box-sizing: border-box;
  }

  h1 {
    font-style: italic;

    text-transform: uppercase;
    font-size: clamp(42px, 8vw, 90px);
    text-shadow:
      0 0 2px #ce5e82,
      0 0 10px #ce5e82;
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

  main {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
</style>
