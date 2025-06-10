<script>
  import CharacterCard from '$lib/components/CharacterCard.svelte';
  import ChatBox from '$lib/components/ChatBox.svelte';
  import { characterStore } from '$lib/stores/character';
</script>

{#if $characterStore}
  <CharacterCard
    imageUrl={$characterStore.character.image_url}
    planetName={$characterStore.character.planet_name}
    characterName={$characterStore.character.name}
  />
{/if}

<ChatBox />
