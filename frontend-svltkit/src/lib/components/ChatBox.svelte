<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { characterStore } from '$lib/stores/character';
	import { get } from 'svelte/store';

	let socket: WebSocket;
	let messages: { from: 'me' | 'ai'; text: string }[] = [];
	let currentAssistantMsg = '';
	let input = '';

	let reconnectDelay = 1000;
	const maxReconnectDelay = 30000;

	let chatWindow: HTMLDivElement; // Reference for scrolling

	function connect() {
		const store = get(characterStore);

		if (!store) {
			console.error('Character store not loaded!');
			return;
		}

		console.log('Trying to connect...');
		socket = new WebSocket(`ws://localhost:8000/chat/${store.thread_id}`);

		socket.addEventListener('open', () => {
			console.log('Connected to WebSocket');
			reconnectDelay = 1000;
		});

		socket.addEventListener('message', (event) => {
			const chunk = event.data;

			if (currentAssistantMsg == '') {
				currentAssistantMsg = chunk;
				messages = [...messages, { from: 'ai', text: currentAssistantMsg }];
			} else {
				currentAssistantMsg += chunk;
				messages[messages.length - 1].text = currentAssistantMsg;
			}

			scrollToBottom();
		});

		socket.addEventListener('close', () => {
			console.log('Disconnected from chat WebSocket');
			reconnect();
		});

		socket.addEventListener('error', (e) => {
			console.error('Websocket error:', e);
			socket.close();
		});
	}

	function reconnect() {
		setTimeout(() => {
			console.log(`Reconnecting after ${reconnectDelay} ms...`);
			connect();
			reconnectDelay = Math.min(reconnectDelay * 2, maxReconnectDelay);
		}, reconnectDelay);
	}

	function sendMessage() {
		if (!input.trim()) return;
		if (socket.readyState == WebSocket.OPEN) {
			currentAssistantMsg = '';
			messages = [...messages, { from: 'me', text: input }];
			socket.send(input);
			input = '';
			scrollToBottom();
		} else {
			console.warn("Can't send message - Websocket is closed.");
		}
	}

	function scrollToBottom() {
		if (chatWindow) {
			chatWindow.scrollTop = chatWindow.scrollHeight;
		}
	}

	onMount(() => {
		connect();
	});

	onDestroy(() => {
		if (socket) socket.close();
	});
</script>

<main>
	<div bind:this={chatWindow} class="chat-window">
		{#each messages as msg}
			<div class={msg.from === 'me' ? 'msg-me' : 'msg-ai'}>
				<p>{msg.text}</p>
			</div>
		{/each}
	</div>

	<div class="input-area">
		<input
			type="text"
			bind:value={input}
			on:keydown={(e) => e.key == 'Enter' && sendMessage()}
			placeholder="Say something..."
		/>
	</div>
</main>

<style>
	.chat-window {
		height: 50vw;
		border: 1px solid #444;
		background: #111;
		color: #f5f5f5;
		overflow-y: auto; /* IMPORTANT for scrolling */
		padding: 1rem;
	}
	.msg-me {
		text-align: right;
		color: #78dce8;
	}
	.msg-ai {
		text-align: left;
		color: #a9dc76;
	}
	.input-area {
		margin-top: 1rem;
	}
	input {
		width: 95%;
		padding: 0.5rem;
		font-size: 1rem;
	}
</style>
