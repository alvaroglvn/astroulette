<script lang="ts">
	// import { onMount } from 'svelte';
	// import { goto } from '$app/navigation';
	// import { characterStore } from '$lib/stores/character';

	// onMount(async () => {
	// 	try {
	// 		const res = await fetch('/api/character/chat');
	// 		if (!res.ok) {
	// 			throw new Error('Failed to load character');
	// 		}

	// 		const data = await res.json();

	// 		characterStore.set({
	// 			thread_id: data.thread_id,
	// 			character: data.character
	// 		});

	// 		await goto('/chat');
	// 	} catch (error) {
	// 		console.error('Error during loading:', error);
	// 		// Optionally redirect back to login if critical
	// 		// await goto('/login');
	// 	}
	// });
</script>

<main class="loading-screen">
	<h1 class="info">Establishing intergalactic uplink</h1>
	<div class="grid-container" aria-hidden="true"></div>
	<div class="grid-fog-bottom" aria-hidden="true"></div>
</main>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');
	:global(html, body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
		font-family: 'Space Grotesk', sans-serif;
		text-align: center;
	}

	.loading-screen {
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
		align-items: center;
	}

	.info {
		font-size: 3.5vw;
		margin-top: 550px;
		color: #ce5e82;
		text-shadow: 0 0 10px rgba(239, 148, 181, 0.341);
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
		background-size: 70px 70px;
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
			background-position: 0 500px;
		}
		to {
			background-position: 0 0;
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
</style>
