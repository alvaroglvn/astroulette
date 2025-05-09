import type { PageServerLoad } from './$types'
import { redirect } from '@sveltejs/kit'
import { PUBLIC_API_URL } from '$env/static/public'

export const load: PageServerLoad = async ({url, fetch}) => {
    const token = url.searchParams.get('token');

    if (!token) {
        throw redirect(302, '/?error=missing-token')
    };

    const res = await fetch(`${PUBLIC_API_URL}/user/verify?token=${token}`, {credentials: 'include'});

    if (!res.ok) {
        throw redirect(302, '/?error=invalid-token');
    }

    throw redirect(302, '/loading')
};