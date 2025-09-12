import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Handle server-side API requests by proxying them to the local FastAPI server
  if (event.url.pathname.startsWith('/api')) {
    // In production, the FastAPI server runs on localhost:8000
    const apiUrl = `http://127.0.0.1:8000${event.url.pathname}${event.url.search}`;

    try {
      console.log(`[SvelteKit] Proxying request to: ${apiUrl}`);

      const response = await fetch(apiUrl, {
        method: event.request.method,
        headers: event.request.headers,
        body:
          event.request.method !== 'GET' ?
            await event.request.arrayBuffer()
          : undefined,
      });

      console.log(`[SvelteKit] Proxy response status: ${response.status}`);
      return response;
    } catch (error) {
      console.error(`[SvelteKit] Proxy error:`, error);
      return new Response('Internal Server Error', { status: 500 });
    }
  }

  const response = await resolve(event);
  return response;
};
