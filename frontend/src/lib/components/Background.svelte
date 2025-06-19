<script lang="ts">
  import { onMount } from 'svelte';

  interface Props {
    starCount?: number;
    matrixDuration?: string;
  }
  let { starCount = 80, matrixDuration = '6s' }: Props = $props();

  type Star = {
    x: number;
    y: number;
    delay: number;
    duration: number;
    size: number;
  };
  let stars: Star[] = $state([]);

  onMount(() => {
    stars = Array.from({ length: starCount }, () => ({
      x: Math.random() * 100, // vw
      y: Math.random() * 50, // vh (clipped to top 50%)
      delay: Math.random() * 5, // seconds
      duration: 2 + Math.random() * 3, // seconds
      size: 1 + Math.random() * 2, // px
    }));
  });

  function getStarStyle(star: Star): string {
    return `
      top: ${star.y}vh;
      left: ${star.x}vw;
      width: ${star.size}px;
      height: ${star.size}px;
      animation-delay: ${star.delay}s;
      animation-duration: ${star.duration}s;
    `;
  }
</script>

<div
  class="background"
  aria-hidden="true"
  style="--matrix-duration: {matrixDuration}"
>
  <div class="starfield">
    {#each stars as star (`${star.x}-${star.y}`)}
      <div class="star" style={getStarStyle(star)}></div>
    {/each}
  </div>
  <div class="matrix"></div>
  <div class="fog"></div>
</div>

<style>
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

  .matrix {
    animation: moveGrid var(--matrix-duration, 1s) linear infinite;
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 50vh;
    background-color: transparent;
    background-image:
      linear-gradient(var(--pink-500) 1px, transparent 2px),
      linear-gradient(to right, var(--pink-500) 1px, transparent 2px);
    /* Use a CSS variable for grid size */
    background-size: var(--grid-size, 70px) var(--grid-size, 70px);
    pointer-events: none;
    transform: perspective(800px) rotateX(60deg);
    transform-origin: top;
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

  .fog {
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
