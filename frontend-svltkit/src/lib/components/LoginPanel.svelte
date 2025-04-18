<script lang="ts">
	import { isLoggedIn } from '$lib/stores/auth';
	const { onLoginSuccess } = $props<{ onLoginSuccess: (email: string) => void }>();
	let username = $state('');
	let email = $state('');
	let isSubmitting = $state(false);
	let errorMsg = $state('');
	let successMsg = $state('');

	async function sendMagicLink() {
		isSubmitting = true;
		try {
			if (!email) {
				errorMsg = 'Email address field is empty';
				return;
			}
			const response = await fetch('/user/login', {
				headers: { 'Content-Type': 'application/json' },
				method: 'POST',
				body: JSON.stringify({ email, username })
			});

			if (response.ok) {
				onLoginSuccess(email);
				isLoggedIn.set(true);
				username = '';
				email = '';
				successMsg = 'Magic link sent! Check your inbox.';
			} else {
				errorMsg = 'Failed to send link. Try again';
			}
		} catch (error) {
			console.error(error);
			errorMsg = 'An unexpected error occurred.';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<main>
	<div class="login-panel">
		<input bind:value={username} placeholder="Your username" />
		<input bind:value={email} type="email" placeholder="Your email" />
		{#if $isLoggedIn}
			<button>Connect!</button>
		{:else}
			<button onclick={sendMagicLink} disabled={!email || isSubmitting}>Submit </button>
		{/if}
		{#if errorMsg}
			<p class="error">{errorMsg}</p>
		{/if}
		{#if successMsg}
			<p class="success">{successMsg}</p>
		{/if}
	</div>
</main>

<style>
	.login-panel {
		background: #1a1a1a;
		color: #e6e6e6;
		font-family: 'Courier New', monospace;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 0 12px rgba(0, 255, 150, 0.2);
		max-width: 400px;
		margin: 2rem auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	input {
		background: #000;
		color: #0f0;
		border: 1px solid #0f0;
		padding: 0.75rem;
		font-size: 1rem;
		font-family: inherit;
	}

	button {
		background: #0f0;
		color: #000;
		border: none;
		padding: 0.75rem;
		font-weight: bold;
		cursor: pointer;
		transition: background 0.2s;
	}

	button:hover {
		background: #00ff7f;
	}

	.error {
		color: #ff5c5c;
		font-size: 0.9rem;
		margin-top: -0.5rem;
	}

	.success {
		color: #00ff7f;
		font-size: 0.9rem;
		margin-top: -0.5rem;
	}
</style>
