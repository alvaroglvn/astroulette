<script>
	import { onMount } from 'svelte';
	import { isLoggedIn } from '$lib/stores/auth';
	import { checkLoginStatus } from '$lib/utils/checkLoginStatus';
	import MachineLayout from '$lib/components/MachineLayout.svelte';

	onMount(async () => {
		const status = await checkLoginStatus();
		isLoggedIn.set(status);
	});
</script>

<main>
	<MachineLayout />
</main>

<style>
</style>
