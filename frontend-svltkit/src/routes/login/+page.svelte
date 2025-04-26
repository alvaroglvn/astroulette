<script lang="ts">
	export let form: {
		error?: string;
		success?: boolean;
	};
	export let data: { error?: string };
</script>

<main class="login-bg">
	<!-- <h1>MarsRoulette</h1> -->
	<form method="POST">
		{#if data.error}
			<p class="form-response error">
				{data.error === 'invalid-token'
					? 'your link is invalid or expired.'
					: 'Something went wrong. Please try again.'}
			</p>
		{/if}
		<h2 class="bleed-subtitle">initiate transplanetary relay</h2>
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
	<div class="grid-container" aria-hidden="true"></div>
	<div class="grid-fog-bottom" aria-hidden="true"></div>
</main>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Space+Grotesk:wght@300..700&display=swap');

	:global(html, body) {
		margin: 0;
		padding: 0;
		height: 100%;
		overflow: hidden;
		font-family: 'Poppins', sans-serif;
	}

	.login-bg {
		background: linear-gradient(
			180deg,
			rgba(18, 7, 36, 1) 0%,
			rgba(32, 13, 58, 1) 66%,
			rgba(46, 71, 112, 1) 100%
		);
		height: 100vh;
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.bleed-subtitle {
		position: absolute;
		top: -1.9em;
		left: 50%;
		transform: translateX(-50%);
		white-space: nowrap;
		color: #ce5e82;
		font-family: 'Space Grotesk', sans-serif;
		font-size: clamp(1rem, 5vw, 3.25rem);
		line-height: 1.1;
		padding: 0 1em;
		z-index: 1;
	}

	form {
		position: relative;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		width: 100%;
		max-width: 50vh;
		padding: 2em;
		font-variant-caps: all-petite-caps;
		background-color: #2e4770;
		border: 9px double #ce5e82;
		z-index: 10;
	}

	form input {
		font-size: 16px;
		font-family: 'Poppins', sans-serif;
		padding: 0.5em;
	}

	form button {
		padding: 0.25em;
		background-color: #eca089;
		font-family: 'Space Grotesk', sans-serif;
		font-size: x-large;
		font-weight: bold;
		font-variant-caps: all-petite-caps;
		cursor: pointer;
	}

	form button:hover {
		background-color: #ecc6a2;
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
			background-position: 0 70px;
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
