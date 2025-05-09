import type { PageServerLoad } from './$types'
import type {CookieSerializeOptions} from 'cookie';
import { redirect } from '@sveltejs/kit'
import { PUBLIC_API_URL } from '$env/static/public'

export const load: PageServerLoad = async ({url, fetch, cookies}) => {
    const token = url.searchParams.get('token');
    console.log('Token received: ', token);

    if (!token) {
        throw redirect(302, '/?error=missing-token')
    };

    const res = await fetch(`${PUBLIC_API_URL}/user/verify?token=${token}`, {credentials: 'include'});

    if (!res.ok) {
        throw redirect(302, '/?error=invalid-token');
    }

    res.headers.get('set-cookie')?.split(',').map(str => {
        const [cookie, ...rest] = str.split(';');
        const [name, value] = cookie.split('=');

        const rawOpts = rest.reduce<Record<string, unknown>>((acc, opt) => {
            const [key, val] = opt.trim().split('=');
            acc[key.toLowerCase()] = val || true;
            return acc;
        }, {});
        const sameSite = rawOpts.samesite?.toString().toLowerCase();
        const opts: CookieSerializeOptions & { path: string; } = {
            domain: 
                import.meta.env.DEV ? 
                undefined :
                rawOpts.domain?.toString(),
            expires: rawOpts.expires ? 
                new Date(rawOpts.expires.toString()) : undefined,
            httpOnly: rawOpts.httponly ? true : undefined,
            maxAge: rawOpts.maxage ? Number(rawOpts.maxage) : undefined,
            partitioned: rawOpts.partitioned ? true : undefined,
            path: rawOpts.path?.toString() ?? '/',
            secure: 
                import.meta.env.DEV ? false : 
                rawOpts.secure ? true : 
                undefined,
            sameSite: 
                sameSite === 'true' ? true :
                sameSite === 'lax' ? 'lax' :
                sameSite === 'strict' ? 'strict' :
                sameSite === 'none' ? 'none' : 
                undefined,
        };
        console.log(name, value, opts);

        cookies.set(name, value, opts);
    });

    console.log('Redirecting to loading page');
    throw redirect(302, '/loading')
};