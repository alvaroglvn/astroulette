import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

/**
 * TODO: I'm pretty sure this layout isn't getting used because there's no pages in this directory or subdirectories. Of course, you don't want to have `/protected` in your route. So you can use (group) routes...
 * https://svelte.dev/docs/kit/advanced-routing#Advanced-layouts-(group)
 *
 * And you end up with files like `/(protected)/chat/+page.svelte`
 */
export const load: LayoutServerLoad = async ({ fetch }) => {
  const res = await fetch(`/api/user/me`, {
    credentials: 'include',
  });

  if (!res.ok) {
    throw redirect(302, '/');
  }

  const user = await res.json();

  return { user };
};
