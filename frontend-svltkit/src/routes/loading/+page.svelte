<script lang="ts">
  import Background from '$lib/components/Background.svelte';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { characterStore } from '$lib/stores/character';

  onMount(async () => {
    try {
      console.log('Loading character...');
      const res = await fetch(`/api/character/chat`, {
        credentials: 'include',
      });
      if (!res.ok) {
        console.error('Character fetch failed:', res.status);
        throw new Error('Failed to load character');
      }

      const data = await res.json();
      console.log('Character loaded:', data);

      characterStore.set({
        thread_id: data.thread_id,
        character: data.character,
        conversation_id: data.conversation_id,
      });

      await goto('/chat');
    } catch (error) {
      console.error('Error during loading:', error);
      await goto('/');
    }
  });
</script>

<main class="loading-screen">
  <Background />
  <h1 class="info">Establishing intergalactic uplink</h1>
</main>

<style>
  /* TODO: Again, fonts and global styles should be in a root +layout. */
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');
  :global(html, body) {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
    font-family: 'Space Grotesk', sans-serif;
  }

  :global(body) {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  :global(*) {
    box-sizing: border-box;
  }

  @keyframes fadeInOut {
    0%,
    100% {
      opacity: 0;
    }
    50% {
      opacity: 1;
    }
  }

  .loading-screen {
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .info {
    font-size: 48px;
    color: #d36b8f;
    text-shadow:
      0 0 2px #ce5e82,
      0 0 10px #ce5e82;
    margin: 0px;
    padding: 0px;
    text-align: center;
    animation: fadeInOut 3s ease-in-out infinite;
  }

  @media (max-width: 768px) {
    .info {
      font-size: 32px;
    }
  }
</style>
