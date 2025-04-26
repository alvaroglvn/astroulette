<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { characterStore } from '$lib/stores/character';

	onMount(async () => {
		try {
			const res = await fetch('/api/character/chat');
			if (!res.ok) {
				throw new Error('Failed to load character');
			}

			const data = await res.json();

			characterStore.set({
				thread_id: data.thread_id,
				character: data.character
			});

			await goto('/chat');
		} catch (error) {
			console.error('Error during loading:', error);
			// Optionally redirect back to login if critical
			// await goto('/login');
		}
	});
</script>

<main class="loading-screen">
	<h1>Establishing uplink...</h1>
	<div class="spinner"></div>
</main>

<style>
	.loading-screen {
		height: 100vh;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background-color: #200d3a;
		color: #ce5e82;
		font-family: 'Space Grotesk', sans-serif;
		text-align: center;
	}

	.spinner {
		margin-top: 2rem;
		width: 50px;
		height: 50px;
		border: 5px solid #ce5e82;
		border-top: 5px solid transparent;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}
</style>
