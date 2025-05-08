import { PUBLIC_API_URL } from "$env/static/public";


export async function FetchChatHistory(threadId: number) {
    const response = await fetch(`${PUBLIC_API_URL}/chat/history/${threadId}`, {credentials: 'include'});
    if (!response.ok) {
        throw new Error(`Failed to fetch chat history: ${response.statusText}`);
    }
    return await response.json();
}