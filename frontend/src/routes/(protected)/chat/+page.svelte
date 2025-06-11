<script>
  import CharacterCard from '$lib/components/CharacterCard.svelte';
  import ChatBox from '$lib/components/ChatBox.svelte';
  import { characterState } from '$lib/stores/character';
</script>

{#if characterState}
  <CharacterCard
    imageUrl={characterState.character.image_url}
    planetName={characterState.character.planet_name}
    characterName={characterState.character.name}
  />
{/if}

<ChatBox />
