<script lang="ts">
  import { goto } from '$app/navigation';
</script>

<!-- TODO: You should probably call this NextCharacterButton. Good practice to end interactive component names with the kind of interactive they are. E.g. EmailInput, PodcastAudio -->
<button
  on:click={() => goto('/loading')}
  aria-label="Connect to a different planet."
>
  Next planet
</button>

<style>
  button {
    grid-column: 2;
    grid-row: 2;
    padding: 0.5em;
    padding-right: 2em;
    max-width: 100%;
    /* TODO: For colors and font families, it's good to use CSS variables. You can declare them on :root {} in your top-level style component */
    background-color: #ecc6a2;
    font-family: 'Space Grotesk', sans-serif;
    font-size: large;
    font-weight: 500;
    border: none;
    cursor: pointer;
    clip-path: polygon(
      0% 0%,
      calc(100% - 20px) 0%,
      100% 50%,
      calc(100% - 20px) 100%,
      0% 100%,
      calc(0% + 20px) 50%
    );
    text-align: right;

    /* TODO: A nice way to device style hierarchy... */
    &:hover {
      background-color: #ecd9c9;
    }
  }

  button:hover {
    background-color: #ecd9c9;
  }
</style>
