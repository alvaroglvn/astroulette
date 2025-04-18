<script lang="ts">
	let { isLoggedIn, onConnect } = $props();
	let label = $derived(() => (isLoggedIn ? 'Connect' : 'Log In'));
</script>

<main>
	<button class="connect" onclick={onConnect}>{label()}</button>
</main>

<style>
	.connect {
		width: 100%;
		padding: 1rem;
		font-weight: bold;
	}
</style>
