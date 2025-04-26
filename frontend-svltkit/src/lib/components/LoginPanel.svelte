<script lang="ts">
	const { isLoggedIn, user, onLoginSuccess } = $props<{
		isLoggedIn: boolean;
		user: { username: string } | null;
		onLoginSuccess: (email: string) => void;
	}>();
	let username = $state('');
	let email = $state('');
	let isSubmitting = $state(false);
	let errorMsg = $state('');
	let successMsg = $state('');

	async function sendMagicLink() {
		isSubmitting = true;
		try {
			const response = await fetch('/user/login', {
				headers: { 'Content-Type': 'application/json' },
				method: 'POST',
				body: JSON.stringify({ email, username })
			});

			if (response.ok) {
				email = '';
				successMsg = 'Link sent! Check your inbox.';
				onLoginSuccess(email);
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
		{#if isLoggedIn && user}
			<p>Welcome back, {user.username}</p>
			<button>Connect!</button>
		{:else if !isLoggedIn}
			<input bind:value={username} placeholder="Your username" />
			<input bind:value={email} type="email" placeholder="Your email" />
			<button>Connect!</button>
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
		background: #ecc6a2;
		padding: 2rem;
		max-width: 300px;
		margin: 2rem auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	input {
		background: #f6f6f6;
		border: 2px solid #eca089;
		padding: 0.75rem;
		font-size: 1rem;
		font-family: inherit;
	}

	button {
		background: #ce5e82;
		color: #000;
		border: none;
		padding: 0.75rem;
		font-weight: bold;
		cursor: pointer;
		transition: background 0.2s;
	}

	button:hover {
		background: #292651;
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
