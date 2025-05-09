import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';

export const load: LayoutServerLoad = async ({ fetch }) => {
    const res = await fetch(`${PUBLIC_API_URL}/user/me`, {
        credentials: 'include',
    });

    if (!res.ok) {
        throw redirect(302, '/');
    }

    const user = await res.json();

    return { user };
};