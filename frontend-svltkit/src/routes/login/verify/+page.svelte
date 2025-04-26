<script lang="ts">
	import { onMount } from 'svelte';

	onMount(() => {
		setTimeout(() => {
			window.location.href = '/loading';
		}, 2000);
	});
</script>

<main class="verify-loading">
	<h2>Establishing uplink...</h2>
	<div class="spinner"></div>
</main>

<style>
	.verify-loading {
		text-align: center;
		color: #ce5e82;
		padding: 4rem;
		font-family: 'Space Grotesk', sans-serif;
	}

	.spinner {
		margin: 2rem auto;
		width: 40px;
		height: 40px;
		border: 3px solid transparent;
		border-top: 3px solid #ce5e82;
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
