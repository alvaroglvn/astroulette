<script lang="ts">
	async function logout() {
		const res = await fetch('/api/user/logout');
		if (res.ok) {
			window.location.href = 'login';
		}
	}
</script>

<button onclick={logout}>Log out</button>
