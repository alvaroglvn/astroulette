<script>
	import Background from '$lib/components/Background.svelte';
	import CharacterCard from '$lib/components/CharacterCard.svelte';
	import ChatBox from '$lib/components/ChatBox.svelte';
	import { characterStore } from '$lib/stores/character';
</script>

<main class="main-placeholder">
	<Background />
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
</main>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');

	:global(html, body) {
		margin: 0;
		padding: 0;
		height: 100vh;
		overflow: hidden;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.character-card {
		width: 35%;
	}

	.chatbox {
		width: 65%;
	}

	.main-placeholder {
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		max-width: 1200px;
		margin: 5em;
		gap: 3em;
		color: #ce5e82;
		font-family: 'Space Grotesk', sans-serif;
	}

	@media (max-width: 1000px) {
		.main-placeholder {
			flex-direction: column;
			padding: 3rem;
			gap: 2rem;
			margin-top: 5em;
			margin-bottom: 5em;
			width: 100%vh;
			height: fit-content;
		}

		.character-card {
			margin: 0 auto;
			width: 100%;
		}

		.chatbox {
			width: 100%;
		}
	}

	@media (max-width: 768px) {
		.main-placeholder {
			padding: 0px;
			margin: 3em;
		}
	}
</style>
