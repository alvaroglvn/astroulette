import type { Actions } from './$types';
import { fail } from '@sveltejs/kit';
import { PUBLIC_API_URL } from '$env/static/public';

export const actions: Actions = {
    default: async ({request, fetch}) => {
        const formData = await request.formData();
        const email = formData.get('email')
        const username = formData.get('username');

        if (typeof email !== 'string' || !email.includes('@')) {
            return fail(400, {error: 'Please enter a valid email address.'});
        }

        if (typeof username !== 'string' || username.trim().length < 3) {
            return fail(400, {error: 'Username must be at least 3 characters.'})
        }

        try {
            const response = await fetch(`${PUBLIC_API_URL}/user/login`, {
                credentials: 'include',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, username })
            });

            if (!response.ok) {
                const errBody = await response.json();
                return fail(response.status, {
                    error: errBody.detail || 'Failed to send magic link.'
                });
            }
            return {success: true};
        } catch(err) {
            console.error('Network error:', err);
            return fail(500, { 
                error: 'Server unavailable. Please try again later.'
            });
        }    
    },
};