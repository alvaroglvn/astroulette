import type { PageServerLoad } from './$types'
import { redirect } from '@sveltejs/kit'

export const load: PageServerLoad = async ({url, fetch}) => {
    const token = url.searchParams.get('token');

    if (!token) {
        throw redirect(302, '/login?error=missing-token')
    };

    const res = await fetch(`/api/user/verify?token=${token}`)

    if (!res.ok) {
        throw redirect(302, '/login?error=invalid-token');
    }

    throw redirect(302, '/loading')
};