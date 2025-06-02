<script lang="ts">
  import { onMount } from 'svelte';

  // Number of stars to generate
  // TODO: Worth considering if star count should be a prop with a default value
  const STAR_COUNT = 80;

  // Array of star settings
  let stars: Array<{
    x: number;
    y: number;
    delay: number;
    duration: number;
    size: number;
  }> = [];

  onMount(() => {
    stars = Array.from({ length: STAR_COUNT }, () => ({
      x: Math.random() * 100, // vw
      y: Math.random() * 50, // vh (clipped to top 50%)
      delay: Math.random() * 5, // seconds
      duration: 2 + Math.random() * 3, // seconds
      size: 1 + Math.random() * 2, // px
    }));
  });
</script>

<!-- TODO: `aria-hidden` only has an effect on elements that contain text/media or elements that are interactive (buttons, fields). Here it's not needed. But if you want, you can put it ONLY on the top-level element. -->
<!-- TODO: `grid-*` classes are a little weird. `matrix`/`fog`? -->
<div class="background">
  <div class="starfield">
    <!-- Key is not STRICTLY needed since this loop only runs once, but it's good practice for loops in component libraries. -->
    {#each stars as star (`${star.x}-${star.y}`)}
      <!-- TODO: You might want to use a function to generate your style attribute -->
      <div
        class="star"
        style="
           top: {star.y}vh;
           left: {star.x}vw;
           width: {star.size}px;
           height: {star.size}px;
           animation-delay: {star.delay}s;
           animation-duration: {star.duration}s;
         "
      ></div>
    {/each}
  </div>
  <div class="grid-container" aria-hidden="true"></div>
  <div class="grid-fog-bottom" aria-hidden="true"></div>
</div>

<style>
  :global(.loading-screen .grid-container) {
    /* TODO: Seems VERY weird to use global and !important. Do you need this? Can you do it with a prop? */
    animation-duration: 1s !important;
  }

  .background {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: -1;
    background: linear-gradient(
      180deg,
      rgba(18, 7, 36, 1) 0%,
      rgba(32, 13, 58, 1) 66%,
      rgba(46, 71, 112, 1) 100%
    );
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .grid-container {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 50vh;
    background-color: transparent;
    background-image:
      linear-gradient(#ce5e82 1px, transparent 2px),
      linear-gradient(to right, #ce5e82 1px, transparent 2px);
    /* Use a CSS variable for grid size */
    background-size: var(--grid-size, 70px) var(--grid-size, 70px);
    pointer-events: none;
    transform: perspective(800px) rotateX(60deg);
    transform-origin: top;
    animation: moveGrid 6s linear infinite;
    z-index: 3;
    opacity: 0.6;
    mask-image: linear-gradient(to top, black 50%, transparent 100%);
    -webkit-mask-image: linear-gradient(to top, black 50%, transparent 100%);
  }

  @keyframes moveGrid {
    from {
      background-position: 0 var(--grid-size, 70px);
    }
    to {
      background-position: 0 0;
    }
  }

  /* Smaller screens: reduce grid size */
  @media (max-width: 600px) {
    :root {
      --grid-size: 40px;
    }
  }

  /* Medium screens: slightly reduced grid size */
  @media (min-width: 601px) and (max-width: 1024px) {
    :root {
      --grid-size: 60px;
    }
  }

  .grid-fog-bottom {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 25vh;
    background: linear-gradient(to top, rgba(18, 7, 36, 1), transparent 100%);
    z-index: 5;
    pointer-events: none;
  }

  .starfield {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    clip-path: inset(0 0 50% 0);
  }

  .star {
    position: absolute;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
    animation-name: blink;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
  }

  @keyframes blink {
    0%,
    100% {
      opacity: 0.8;
    }
    50% {
      opacity: 0.2;
    }
  }
</style>
