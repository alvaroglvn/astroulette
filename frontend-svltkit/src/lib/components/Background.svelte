<div class="background">
	<div class="bg"></div>
	<div class="starfield"></div>
	<div class="grid-container" aria-hidden="true"></div>
	<div class="grid-fog-bottom" aria-hidden="true"></div>
</div>

<style>
	.background {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: -1;
	}
	.bg {
		background: linear-gradient(
			180deg,
			rgba(18, 7, 36, 1) 0%,
			rgba(32, 13, 58, 1) 66%,
			rgba(46, 71, 112, 1) 100%
		);
		height: 100vh;
		width: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.grid-container {
		position: absolute;
		bottom: 0;
		width: 100%;
		height: 50vh;
		background-color: transparent;
		background-image:
			linear-gradient(#ce5e82 1px, transparent 2px),
			linear-gradient(to right, #ce5e82 1px, transparent 2px);
		background-size: 70px 70px;
		pointer-events: none;
		transform: perspective(800px) rotateX(60deg);
		transform-origin: top;
		animation: moveGrid 6s linear infinite;
		z-index: 3;
		opacity: 0.6;
		mask-image: linear-gradient(to top, black 50%, transparent 100%);
		-webkit-mask-image: linear-gradient(to top, black 50%, transparent 100%);
	}

	@keyframes moveGrid {
		from {
			background-position: 0 70px;
		}
		to {
			background-position: 0 0;
		}
	}

	.grid-fog-bottom {
		position: absolute;
		bottom: 0;
		width: 100%;
		height: 25vh;
		background: linear-gradient(to top, rgba(18, 7, 36, 1), transparent 100%);
		z-index: 5;
		pointer-events: none;
	}

	.starfield {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: transparent;
		overflow: hidden;
		clip-path: inset(0 0 50% 0);
	}

	.starfield::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 2px;
		height: 2px;
		background: white;
		box-shadow:
			20vw 30vh white,
			50vw 80vh white,
			70vw 60vh white,
			90vw 20vh white,
			10vw 50vh white,
			30vw 70vh white,
			80vw 40vh white,
			60vw 10vh white,
			25vw 85vh white,
			75vw 15vh white,
			15vw 20vh white,
			40vw 45vh white,
			55vw 35vh white,
			85vw 90vh white,
			95vw 65vh white,
			5vw 80vh white,
			35vw 5vh white,
			45vw 50vh white,
			65vw 25vh white,
			50vw 95vh white;
	}
</style>
