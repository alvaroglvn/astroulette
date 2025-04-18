<script lang="ts">
	import CharacterCard from './CharacterCard.svelte';
	import ChatBox from './ChatBox.svelte';
	import LoginPanel from './LoginPanel.svelte';
	import { isLoggedIn } from '$lib/stores/auth';
</script>

<main>
	<div class="shell">
		<div class="character-panel">
			<CharacterCard />
		</div>
		<div class="chat-panel">
			{#if $isLoggedIn}
				<ChatBox />
			{:else}
				<LoginPanel onLoginSuccess={(email) => isLoggedIn.set(true)} />
			{/if}
		</div>
	</div>
</main>

<style>
	.shell {
		display: flex;
		flex-direction: row;
		width: 100%;
		height: 50vh;
		max-width: 1200px;
		margin: 0 auto;
		overflow-y: auto;
	}

	.character-panel {
		width: 35%;
		padding: 1rem;
		box-sizing: border-box;
		background-color: #f5f5f5;
		border-right: 1px solid #ccc;
	}

	.chat-panel {
		width: 65%;
		padding: 1rem;
		box-sizing: border-box;
		background-color: #ffffff;
	}

	@media (max-width: 768px) {
		.shell {
			flex-direction: column;
		}

		.character-panel,
		.chat-panel {
			width: 100%;
		}
	}
</style>
