<script lang="ts">
	let {
		name = 'John Carter',
		planet = 'Barsoom',
		imageUrl = 'https://cdn.leonardo.ai/users/1b5cfba4-58d0-4084-9594-f5e2c086b961/generations/eb4d3843-e905-4a20-a57a-d20e5f0e5aa2/Leonardo_Phoenix_10_Frontal_closeup_of_a_male_cyborg_galactic_0.jpg',
		description = 'Warlord of Mars'
	} = $props();
</script>

<main>
	<div class="character_card">
		<img class="portrait" src={imageUrl} alt={description} aria-label={`Portrait of ${name}`} />
		<h1>{name}</h1>
		<h2>{planet}</h2>
		<p>{description}</p>
	</div>
</main>

<style>
	.character_card {
		text-align: center;
		padding: 2rem;
		margin: 1rem;
		border: 1px solid black;
		box-shadow: 5px 3px 3px gray;
		border-radius: 0.25rem;
	}
	.portrait {
		border-radius: 50%;
		max-width: 150px;
		width: 60%;
		object-fit: cover;
		margin: 0 auto;
		display: block;
		border: 2px solid teal;
	}

	@media (min-width: 768px) {
		.character_card {
			max-width: fit-content;
			margin-right: auto;
		}
	}
</style>
