type ChatMessages = Array<{
    role: string;
    content: string;
    created_at: string;
}>;

export async function fetchChatHistory(threadId: number) {
    const response = await fetch(`/api/chat/history/${threadId}`, {credentials: 'include'});
    if (!response.ok) {
        throw new Error(`Failed to fetch chat history: ${response.statusText}`);
    }
    return await response.json() as ChatMessages;
}