<script lang="ts">
	export let imageUrl: string;
	export let planetName: string;
	export let characterName: string;
</script>

<div class="character-container">
	<div class="character-card">
		<img src={imageUrl} alt="Character portrait" class="character-image" />
		<div class="character-info">
			<p>
				Now chatting with:<br /> <strong><span class="info_word">{characterName}</span></strong>
			</p>
		</div>
	</div>
	<div class="planet-info">
		<p>Planet: <strong><span class="info_word">{planetName}</span></strong></p>
	</div>
	<button>Next planet</button>
</div>

<style>
	.character-container {
		max-width: clamp(450px, 100%, 350px);
		margin: 0;
		padding: 0;
	}
	.character-card {
		position: relative;
		padding: 0.25em;
		background: linear-gradient(
			to bottom,
			/* Light edge */ #2e4770 0%,
			/* Mid shoulder */ #292651 10%,
			/* Dark center */ #200d3a 50%,
			/* Mid shoulder */ #292651 90%,
			/* Light edge */ #2e4770 100%
		);

		/* darker pink glow */
		box-shadow:
			0 0 0 4px #d36b8f,
			0 0 6px #d36b8f,
			0 0 12px #d36b8f,
			0 0 18px #d36b8f;
	}

	.character-image {
		position: absolute;
		top: -75px;
		left: -40px;
		margin-bottom: 0;
		border-radius: 42%;
		width: clamp(100px, 20vw, 150px);
		box-shadow:
			0 0 0 4px #d36b8f,
			0 0 6px #d36b8f,
			0 0 12px #d36b8f,
			0 0 18px #d36b8f;
	}

	.character-info {
		text-align: right;
		font-size: 20px;
		margin-right: 0.45em;
	}

	.planet-info {
		font-size: 20px;
		text-align: center;
		margin-top: 2em;

		background: linear-gradient(
			to bottom,
			/* Light edge */ #2e4770 0%,
			/* Mid shoulder */ #292651 10%,
			/* Dark center */ #200d3a 50%,
			/* Mid shoulder */ #292651 90%,
			/* Light edge */ #2e4770 100%
		);

		box-shadow:
			0 0 0 4px #d36b8f,
			0 0 6px #d36b8f,
			0 0 12px #d36b8f,
			0 0 18px #d36b8f;
	}

	.planet-info p {
		padding: 0.5em;
	}

	.info_word {
		color: #ecc6a2;
	}

	button {
		margin-top: 1em;
		padding: 0.5em;
		padding-right: 2em;
		width: fit-content;
		background-color: #ecc6a2;
		font-family: 'Space Grotesk', sans-serif;
		font-size: large;
		font-weight: 500;
		border: none;
		cursor: pointer;
		clip-path: polygon(0% 0%, calc(100% - 20px) 0%, 100% 50%, calc(100% - 20px) 100%, 0% 100%);
	}

	button:hover {
		background-color: #ecd9c9;
	}

	@media (max-width: 1048px) {
		.character-container {
			max-width: clamp(450px, 100%, 350px);
			margin: 0;
			padding: 0;
			display: flex;
			flex-direction: column;
			align-items: center;
		}

		.character-image {
			position: absolute;
			top: -125px;
			left: 50%;
			transform: translateX(-50%);
		}

		.character-card {
			padding: 0;
			width: 100%;
		}

		.character-card p {
			margin-top: 2.25em;
			text-align: center;
		}

		.planet-info {
			width: 100%;
			margin-top: 1.5em;
		}

		button {
			width: 100%;
			margin-top: 1.5em;
		}
	}
</style>
