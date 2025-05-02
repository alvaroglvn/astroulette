<script lang="ts">
	export let imageUrl: string;
	export let planetName: string;
	export let characterName: string;
</script>

<div class="character-card">
	<img src={imageUrl} alt="Character portrait" class="character-image" />
	<div class="character-info">
		<p>Connected to planet:<br /> <strong><span class="info_word">{planetName}</span></strong></p>
		<p>Now chatting with:<br /> <strong><span class="info_word">{characterName}</span></strong></p>
	</div>
</div>

<style>
	.character-card {
		padding: 1.5em;
		background-color: #292651;
		border-radius: 0.25em;
		border: 9px double #ce5e82;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.character-image {
		width: 80%;
		height: auto;
		border-radius: 0.25em;
		margin-bottom: 1em;
		border: 9px double #ce5e82;
	}

	.character-info {
		text-align: center;
		font-size: 20px;
	}

	.info_word {
		color: #ecc6a2;
	}
</style>
