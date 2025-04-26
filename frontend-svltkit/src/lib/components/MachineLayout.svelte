<script lang="ts">
	import CharacterCard from './CharacterCard.svelte';
	import ChatBox from './ChatBox.svelte';
	import LoginPanel from './LoginPanel.svelte';
	import { isLoggedIn } from '$lib/stores/auth';

	let user: { username: string } | null = null;

	async function onLoginSuccess(email: string) {
		try {
			const response = await fetch('/user/me', {
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include'
			});
			if (response.ok) {
				const data = await response.json();
				user = data;
				isLoggedIn.set(true);
			}
		} catch (error) {
			console.error('Failed to fetch user', error);
		}
	}
</script>

<main>
	<div class="shell">
		<div class="character-panel">
			<CharacterCard />
		</div>
		<div class="chat-panel">
			<ChatBox />
		</div>
	</div>
</main>

<style>
	.shell {
		margin: 2em;
		padding: 2em;
		display: flex;
		flex-direction: row;
		justify-content: center;
		gap: 2em;
		background-color: #292651;
	}

	.chat-panel {
		width: 65%;
		height: fit-content;
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
