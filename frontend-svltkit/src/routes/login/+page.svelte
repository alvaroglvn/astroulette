<script lang="ts">
	import Background from '$lib/components/Background.svelte';
	import LoginForm from '$lib/components/LoginForm.svelte';
	export let data;
	export let form;
</script>

<main>
	<Background />
	<LoginForm {data} {form} />
</main>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap');

	:global(html, body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
		font-family: 'Space Grotesk', sans-serif;
	}

	:global(*) {
		box-sizing: border-box;
	}

	main {
		position: relative;
		width: 100vw;
		height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
