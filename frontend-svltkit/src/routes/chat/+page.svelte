<script>
	import CharacterCard from '$lib/components/CharacterCard.svelte';
	import ChatBox from '$lib/components/ChatBox.svelte';
	import { characterStore } from '$lib/stores/character';
</script>

<main class="main-placeholder">
	<div class="character-card">
		{#if $characterStore}
			<CharacterCard
				imageUrl={$characterStore.character.image_url}
				planetName={$characterStore.character.planet_name}
				characterName={$characterStore.character.name}
			/>
		{/if}
	</div>
	<div class="chatbox">
		<ChatBox />
	</div>

	<div class="grid-container" aria-hidden="true"></div>
	<div class="grid-fog-bottom" aria-hidden="true"></div>
</main>

<style>
	:global(html, body) {
		margin: 0;
		padding: 0;
		height: 100%;
		overflow: hidden;
		font-family: 'Poppins', sans-serif;
		background: linear-gradient(
			180deg,
			rgba(18, 7, 36, 1) 0%,
			rgba(32, 13, 58, 1) 66%,
			rgba(46, 71, 112, 1) 100%
		);
	}

	.character-card {
		width: 35%;
		z-index: 1;
	}

	.chatbox {
		width: 65%;
		background-color: #2e4770;
		border-radius: 0.25em;
		border: 9px double #ce5e82;
		z-index: 1;
	}

	.main-placeholder {
		padding: 3rem;
		height: 100vh;
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 2rem;
		color: #ce5e82;
		font-family: 'Space Grotesk', sans-serif;
		font-size: 2rem;
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
		opacity: 0.6;
		mask-image: linear-gradient(to top, black 50%, transparent 100%);
		-webkit-mask-image: linear-gradient(to top, black 50%, transparent 100%);
	}

	.grid-fog-bottom {
		position: absolute;
		bottom: 0;
		width: 100%;
		height: 25vh;
		background: linear-gradient(to top, rgba(18, 7, 36, 1), transparent 100%);
		pointer-events: none;
	}
</style>
