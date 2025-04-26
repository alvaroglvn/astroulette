import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ fetch }) => {
    const res = await fetch('/api/user/me');

    if (!res.ok) {
        throw redirect(302, '/login');
    }

    const user = await res.json();

    return { user };
};