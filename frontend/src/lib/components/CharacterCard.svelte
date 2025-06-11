<script lang="ts">
  export let imageUrl: string;
  export let planetName: string;
  export let characterName: string;

  import NextCharacter from './NextCharacterButton.svelte';
</script>

<div class="character-container">
  <img src={imageUrl} alt="Character portrait" class="character-image" />
  <div class="character-card">
    <dl>
      <dt>Name</dt>
      <dd>{characterName}</dd>
      <dt>Planet</dt>
      <dd>{planetName}</dd>
    </dl>
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
    color: var(--pink-500);
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
    box-shadow:
      0 0 0 4px #d36b8f,
      0 0 6px #d36b8f,
      0 0 12px #d36b8f,
      0 0 18px #d36b8f;
    font-family: var(--font-display);
  }

  dl {
    margin: 0;
  }

  dt {
    font-weight: bold;
    display: inline;
  }

  /* Use a pseudo-element to append a colon after each definition term */
  dt::after {
    content: ':';
    margin-right: 0.25rem;
  }

  dd {
    display: inline;
    margin: 0 1rem 0 0;
  }
</style>
