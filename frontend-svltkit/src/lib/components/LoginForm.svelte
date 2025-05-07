<script lang="ts">
	export let form: {
		error?: string;
		success?: boolean;
	} | null;
	export let data: { error?: string | null };
</script>

<div class="login-form">
	<h3>Begin interplanetary relay</h3>
	<form method="POST">
		{#if data.error}
			<p class="form-response error">
				{data.error === 'invalid-token'
					? 'your link is invalid or expired.'
					: 'Something went wrong. Please try again.'}
			</p>
		{/if}
		<!-- <h2 class="bleed-subtitle">initiate transplanetary relay</h2> -->
		<input
			name="username"
			type="text"
			placeholder="Your username"
			autocomplete="username"
			required
		/>

		<input name="email" type="email" placeholder="Your email" autocomplete="email" required />

		<button type="submit">Let's go!</button>

		{#if form?.error}
			<p class="error-msg">{form.error}</p>
		{/if}
		{#if form?.success}
			<p class="success-msg">Check your email for your login link</p>
		{/if}
	</form>
</div>

<style>
	.login-form {
		width: 65vw;
		max-width: 550px;
	}
	h3 {
		font-size: clamp(18px, 4vw, 34px);
		color: #ce5e82;
		text-transform: uppercase;
		text-align: center;
		display: block;
		margin: 0;
		line-height: 0.73em;
	}
	form {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding: 2em;
		background-color: #2e4770;
		border: 9px double #ce5e82;
	}

	form input {
		font-size: 16px;
		padding: 0.5em;
	}

	form button {
		padding: 0.25em;
		background-color: #ecc6a2;
		font-family: 'Space Grotesk', sans-serif;
		font-size: x-large;
		font-weight: bold;
		cursor: pointer;
		border: none;
	}

	form button:hover {
		background-color: #eca089;
	}

	.error-msg {
		text-align: center;
		color: #ce5e82;
		font-size: 3vw;
	}

	.success-msg {
		text-align: center;
		color: #ecc6a2;
		font-size: clamp(1.8rem, 2.5vw, 2rem);
		line-height: clamp(0.5rem, 5vw, 2rem);
	}

	.form-response.error {
		text-align: center;
		color: #ce5e82;
		font-size: clamp(1.8rem, 2.5vw, 2rem);
	}
</style>
