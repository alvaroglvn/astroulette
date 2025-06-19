import { array, object, string, number, parse } from 'valibot';

const ChatMessageSchema = object({
  role: string(),
  content: string(),
  created_at: number(), // Change from string() to number()
});

const ChatMessagesSchema = array(ChatMessageSchema);

export async function fetchChatHistory(threadId: number) {
  const response = await fetch(`/api/chat/history/${threadId}`, {
    credentials: 'include',
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch chat history: ${response.statusText}`);
  }
  const data = await response.json();
  console.log('API response:', data); // Debugging
  // Validate that the response is an array
  if (!Array.isArray(data)) {
    throw new Error('Invalid API response: Expected an array');
  }
  return parse(ChatMessagesSchema, data);
}
