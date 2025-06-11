<script lang="ts">
  /* eslint-disable svelte/no-at-html-tags */
  import { onMount, onDestroy } from 'svelte';
  import { characterState } from '$lib/stores/character';
  import { fetchChatHistory } from '$lib/api/chat';
  import { PUBLIC_FRONTEND_URL } from '$env/static/public';

  let socket: WebSocket;
  let messages: { from: 'me' | 'ai'; text: string }[] = [];
  let currentAssistantMsg = '';
  let input = '';

  let reconnectDelay = 1000;
  const maxReconnectDelay = 30000;

  let chatWindow: HTMLDivElement; // Reference for scrolling

  let isDisconnected = false;

  function connect() {
    const store = characterState;
    if (!store || !store.thread_id) {
      console.warn(
        '[ChatBox] Missing character store or thread_id — skipping connect',
      );
      return;
    }

    console.log('Trying to connect...');
    const base = new URL(PUBLIC_FRONTEND_URL);
    base.protocol = base.protocol === 'https:' ? 'wss:' : 'ws:';
    base.pathname = `/api/chat/${store.thread_id}`;
    const wsURL = base.toString();
    socket = new WebSocket(wsURL);

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
    const store = characterState;
    if (!store || !store.thread_id) {
      console.error('Character store not loaded or missing thread_id');
      return;
    }

    try {
      const history = await fetchChatHistory(store.thread_id);

      messages = history.map((entry: { role: string; content: string }) => ({
        from: entry.role === 'user' ? 'me' : 'ai',
        text: entry.content,
      }));
      scrollToBottom();
      currentAssistantMsg = '';
    } catch (err) {
      console.error('Error loading chat history:', err);
    }
  }

  onMount(() => {
    const path = window.location.pathname;
    if (path !== '/chat') {
      console.log('[ChatBox] Aborting — not on /chat');
      return;
    }
    loadHistory().then(connect);
  });

  onDestroy(() => {
    if (socket) socket.close();
  });
</script>

<div class="chatbox">
  {#if isDisconnected}
    <p>Connection lost... Trying to reconnect</p>
  {/if}

  <div bind:this={chatWindow} class="chat-window">
    {#each messages as msg, i (i)}
      <div
        class={{
          'msg': true,
          'msg-me': msg.from == 'me',
          'msg-ai': msg.from == 'ai',
        }}
      >
        {@html msg.text.replace(/(?:\r\n|\r|\n)/g, '<br />')}
      </div>
    {/each}
  </div>

  <input
    type="text"
    bind:value={input}
    on:keydown={(e) => e.key == 'Enter' && sendMessage()}
    placeholder="Say something..."
  />
</div>

<style>
  .chatbox {
    display: flex;
    flex-direction: column;
    justify-content: stretch;
    align-items: stretch;
    width: 100%;
    height: 100%;
    max-height: 100%;
  }
  .chat-window {
    flex: 1 1 0px;
    overflow-y: auto; /* IMPORTANT for scrolling */
    padding: 1.5rem 1rem;
    font-family: var(--font-display);
    display: flex;
    flex-direction: column;

    font-size: clamp(14px, 2vw, 18px);
    background-color: #f6f6f6;
    box-shadow:
      0 0 0 4px --var(--pink-500),
      0 0 6px --var(--pink-500),
      0 0 12px --var(--pink-500),
      0 0 18px --var(--pink-500);
    width: 100%;
  }

  .msg {
    padding: 0.5rem 1rem;
    font-family: var(--font-display);
  }
  .msg-me {
    width: max-content;
    max-width: calc(100% - 3rem);
    border-radius: 1rem 1rem 0 1rem;
    border: 0.15rem solid --var(--pink-500);
    align-self: end;
    font-family: var(--font-display);
  }
  .msg-ai {
    width: max-content;
    max-width: calc(100% - 3rem);
    border-radius: 1rem 1rem 1rem 0;
    border: 0.15rem solid #2e4770;
    font-family: var(--font-display);
  }

  .msg-me + .msg-me,
  .msg-ai + .msg-ai {
    margin-top: 0.25rem;
  }
  .msg-me + .msg-ai,
  .msg-ai + .msg-me {
    margin-top: 1.5rem;
  }

  .msg-me + .msg-me {
    border-top-right-radius: 0;
  }
  .msg-ai + .msg-ai {
    border-top-left-radius: 0;
  }

  input {
    flex: 0 0 auto;
    box-sizing: border-box;
    background-color: #f6f6f6;
    margin-top: 0.25rem;
    width: 100%;
    padding: 0.5rem;
    font-size: clamp(14px, 2vw, 18px);
    font-family: var(--font-display);
    border: 0;

    box-shadow:
      0 0 0 4px --var(--pink-500),
      0 0 6px --var(--pink-500),
      0 0 12px --var(--pink-500),
      0 0 18px --var(--pink-500);
  }
</style>
