<script lang="ts">
  export let imageUrl: string;
  export let planetName: string;
  export let characterName: string;

  import NextCharacter from './NextCharacter.svelte';
</script>

<div class="character-container">
  <img src={imageUrl} alt="Character portrait" class="character-image" />
  <div class="character-card">
    <p>
      User: <strong><span class="info_word">{characterName}</span></strong>
    </p>
    <p>Planet: <strong><span class="info_word">{planetName}</span></strong></p>
  </div>
  <NextCharacter />
</div>

<style>
  .character-container {
    width: 100%;
    display: grid;
    grid-template-columns: 150px auto;
    grid-template-rows: auto auto;
    gap: 1.25rem;
  }

  .character-image {
    grid-column: 1;
    grid-row: 1 / 3;
    position: relative;
    z-index: 1;
    border-radius: 30% 0 30% 30%;
    width: 150px;
    box-shadow:
      0 0 0 4px #d36b8f,
      0 0 6px #d36b8f,
      0 0 12px #d36b8f,
      0 0 18px #d36b8f;
  }

  .character-card {
    grid-column: 2;
    grid-row: 1;
    position: relative;
    padding: 0.25rem;
    padding-left: calc(75px + 1.25rem);
    left: calc(-1rem);
    width: calc(100% + 1rem);
    font-size: 20px;
    color: #d36b8f;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: linear-gradient(
      to bottom,
      /* Light edge */ #2e4770 0%,
      /* Mid shoulder */ #292651 10%,
      /* Dark center */ #200d3a 50%,
      /* Mid shoulder */ #292651 90%,
      /* Light edge */ #2e4770 100%
    );

    /* darker pink glow */
    box-shadow:
      0 0 0 4px #d36b8f,
      0 0 6px #d36b8f,
      0 0 12px #d36b8f,
      0 0 18px #d36b8f;
  }

  p {
    margin: 0;
  }

  .info_word {
    color: #ecc6a2;
  }
</style>
