type ChatMessages = Array<{
  role: string;
  content: string;
  created_at: string;
}>;

export async function fetchChatHistory(threadId: number) {
  const response = await fetch(`/api/chat/history/${threadId}`, {
    credentials: 'include',
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch chat history: ${response.statusText}`);
  }
  // TODO: You might want to assert the type using a library like valibot
  return (await response.json()) as ChatMessages;
}
