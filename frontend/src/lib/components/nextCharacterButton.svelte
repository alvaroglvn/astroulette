<script lang="ts">
  import { goto } from '$app/navigation';
</script>

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

    background-color: --var(--soft-yellow);
    font-family: --var(--font-display);
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

    &:hover {
      background-color: #ecd9c9;
    }
  }
</style>
