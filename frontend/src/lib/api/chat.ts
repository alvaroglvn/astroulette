import { array, object, string, parse } from 'valibot';

const ChatMessageSchema = object({
  role: string(),
  content: string(),
  created_at: string(),
});

const ChatMessagesSchema = array(ChatMessageSchema);

export async function fetchChatHistory(threadId: number) {
  const response = await fetch(`/api/chat/history/${threadId}`, {
    credentials: 'include',
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch chat history: ${response.statusText}`);
  }
  return parse(ChatMessagesSchema, await response.json());
}
