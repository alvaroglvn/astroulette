<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { characterStore } from '$lib/stores/character';
	import { get } from 'svelte/store';
	import { FetchChatHistory } from '$lib/api/chat';

	let socket: WebSocket;
	let messages: { from: 'me' | 'ai'; text: string }[] = [];
	let currentAssistantMsg = '';
	let input = '';

	let reconnectDelay = 1000;
	const maxReconnectDelay = 30000;

	let chatWindow: HTMLDivElement; // Reference for scrolling

	let isDisconnected = false;

	function connect() {
		const store = get(characterStore);

		if (!store || !store.thread_id) {
			console.error('Character store not loaded or missing thread_id!');
			return;
		}

		console.log('Trying to connect...');
		socket = new WebSocket(`ws://localhost:8000/chat/${store.thread_id}`);

		socket.addEventListener('open', () => {
			console.log('Connected to WebSocket');
			reconnectDelay = 1000;
			isDisconnected = false;
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
			isDisconnected = true;
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

	async function loadHistory() {
		const store = get(characterStore);
		if (!store || !store.thread_id) {
			console.error('Character store not loaded or missing thread_id');
			return;
		}

		try {
			const history = await FetchChatHistory(store.thread_id);
			messages = history.map((entry: any) => ({
				from: entry.role === 'user' ? 'me' : 'ai',
				text: entry.content
			}));
			scrollToBottom();
			currentAssistantMsg = '';
		} catch (err) {
			console.error('Error loading chat history:', err);
		}
	}

	onMount(() => {
		loadHistory().then(connect);
	});

	onDestroy(() => {
		if (socket) socket.close();
	});
</script>

<main>
	{#if isDisconnected}
		<p>Connection lost... Trying to reconnect</p>
	{/if}
	<div bind:this={chatWindow} class="chat-window">
		{#each messages as msg}
			<div class={msg.from === 'me' ? 'msg-me' : 'msg-ai'}>
				<p>{msg.text}</p>
			</div>
		{/each}
	</div>

	<input
		type="text"
		bind:value={input}
		on:keydown={(e) => e.key == 'Enter' && sendMessage()}
		placeholder="Say something..."
	/>
</main>

<style>
	.chat-window {
		height: 30vw;
		overflow-y: auto; /* IMPORTANT for scrolling */
		padding: 2rem;
		font-size: clamp(12px, 3vw, 18px);
		background-color: #200d3a;
		box-shadow:
			0 0 0 4px #d36b8f,
			0 0 6px #d36b8f,
			0 0 12px #d36b8f,
			0 0 18px #d36b8f;
	}
	.msg-me {
		text-align: right;
		color: #eca089;
	}
	.msg-ai {
		text-align: left;
		color: #ecc6a2;
	}
	/* .input-area {
		margin-top: 0;
		padding: 1rem;
		background-color: #ce5e82;
	} */
	input {
		box-sizing: border-box;
		width: 100%;
		margin-top: 2em;
		padding: 0.5rem;
		font-size: 18px;
		border: 0;

		box-shadow:
			0 0 0 4px #d36b8f,
			0 0 6px #d36b8f,
			0 0 12px #d36b8f,
			0 0 18px #d36b8f;
	}
</style>
