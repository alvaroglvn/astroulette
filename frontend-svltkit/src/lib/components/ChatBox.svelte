<script lang="ts">
	let messages = $state([
		{ id: 1, sender: 'user', text: 'Hello' },
		{ id: 2, sender: 'assistant', text: 'Good day to you!' }
	]);
	let currentMessage = $state('');
	let isTyping = $state(false);
	let bottomRef = $state<HTMLDivElement>();

	$effect(() => {
		scrollToBottom();
	});

	function scrollToBottom() {
		if (bottomRef) {
			bottomRef.scrollIntoView({ behavior: 'smooth' });
		}
	}

	function sendMessage() {
		if (currentMessage.trim().length > 0) {
			const newMessage = {
				id: Date.now(),
				sender: 'user',
				text: currentMessage
			};
			messages = [...messages, newMessage];
			currentMessage = '';
			isTyping = true;

			setTimeout(() => {
				const assistantMessage = {
					id: Date.now() + 1,
					sender: 'assistant',
					text: 'This is a mock assistant reply!'
				};
				isTyping = false;
				messages = [...messages, assistantMessage];
			}, 1000);
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key == 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}
</script>

<main>
	<div class="chat-scroll">
		{#each messages as message (message.id)}
			<div
				class="chat-message"
				class:user-message={message.sender === 'user'}
				class:assistant-message={message.sender === 'assistant'}
			>
				{message.text}
			</div>
		{/each}

		{#if isTyping}
			<div class="chat-message assistant-message typing-indicator">
				Assistant is typing<span class="dots">
					<span>.</span><span>.</span><span>.</span>
				</span>
			</div>
		{/if}

		<div bind:this={bottomRef}></div>
	</div>
	<textarea bind:value={currentMessage} onkeydown={handleKeydown} aria-label="Type your message"
	></textarea>
	<button onclick={sendMessage} disabled={currentMessage.trim() === ''}>Send</button>
</main>

<style>
	.chat-message {
		padding: 0.5rem 1rem;
		margin-bottom: 0.5rem;
		border-radius: 1rem;
		max-width: 70%;
		line-height: 1.4;
		font-size: 0.95rem;
		word-wrap: break-word;
	}

	.user-message {
		background-color: #d0f0ff;
		align-self: flex-end;
		text-align: right;
		border: 1px solid #3399cc;
	}

	.assistant-message {
		background-color: #eee;
		align-self: flex-start;
		text-align: left;
		border: 1px solid #bbb;
	}

	.chat-scroll {
		max-height: 300px;
		overflow-y: auto;
		margin-bottom: 1rem;
		display: flex;
		flex-direction: column;
	}

	.typing-indicator .dots span {
		animation: blink 1.5s infinite;
		opacity: 0;
	}

	.typing-indicator .dots span:nth-child(1) {
		animation-delay: 0s;
	}

	.typing-indicator .dots span:nth-child(2) {
		animation-delay: 0.2s;
	}

	.typing-indicator .dots span:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes blink {
		0%,
		80%,
		100% {
			opacity: 0;
		}
		40% {
			opacity: 1;
		}
	}
</style>
