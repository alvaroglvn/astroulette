<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { isLoggedIn } from '$lib/stores/auth';

	let isVerifying = $state(true);
	let errorMsg = $state('');

	$effect(() => {
		const token = page.url.searchParams.get('token');

		const run = async () => {
			if (!token) {
				errorMsg = 'No token found in the URL.';
				isVerifying = false;
				return;
			}

			try {
				const response = await fetch('/user/verify', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ token })
				});

				if (response.ok) {
					isLoggedIn.set(true);
					await goto('/');
				} else {
					errorMsg = 'Verification failed.';
				}
			} catch (err) {
				errorMsg = 'Something went wrong.';
				console.error(err);
			} finally {
				isVerifying = false;
			}
		};

		run();
	});
</script>
