<script lang="ts">
  export let data: {
    user: {
      id: number;
      username: string;
      email: string;
    };
  };
</script>

<header>
  Logged in as {data.user.username}
</header>

<slot />
