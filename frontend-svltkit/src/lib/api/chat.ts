export async function FetchChatHistory(threadId: number) {
    const response = await fetch(`api/chat/history/${threadId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch chat history: ${response.statusText}`);
    }
    return await response.json();
}