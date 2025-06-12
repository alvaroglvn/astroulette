<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { characterState } from '$lib/stores/character';

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

      characterState.set({
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

<h1 class="info">Establishing intergalactic uplink</h1>

<style>
  .info {
    font-size: 48px;
    color: var(--pink-500);
    text-shadow:
      0 0 2px var(--pink-500),
      0 0 10px var(--pink-500);
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
