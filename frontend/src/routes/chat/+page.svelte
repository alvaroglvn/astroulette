<script>
  import Background from '$lib/components/Background.svelte';
  import CharacterCard from '$lib/components/CharacterCard.svelte';
  import ChatBox from '$lib/components/ChatBox.svelte';
  import { characterStore } from '$lib/stores/character';
</script>

<Background />

<main>
  {#if $characterStore}
    <CharacterCard
      imageUrl={$characterStore.character.image_url}
      planetName={$characterStore.character.planet_name}
      characterName={$characterStore.character.name}
    />
  {/if}

  <ChatBox />
</main>

<style>
  /* TODO: Strange to see fonts and global styles here */
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');

  :global(html, body) {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
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
    align-items: start;
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
