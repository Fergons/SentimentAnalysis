import type {PageServerLoad, Actions} from './$types';
import {redirect, error} from '@sveltejs/kit';
import {signin} from '$lib/server/api/auth';
import {coo} from "$app/stores";


export const load: PageServerLoad = (event) => {
    if (event.locals.authenticated) {
        throw redirect(302, '/');
    }
};


export const actions: Actions = {
    default: async (event) => {
        const formData = Object.fromEntries(await event.request.formData());
        console.log(formData)
        if (!formData.email || !formData.password) {
            throw error(400, {
                message: 'Missing email or password'
            });
        }

        const {email, password} = formData as { email: string; password: string };

        try {
            const token = await signin(email, password);

             event.cookies.set('access_token', `Bearer ${token}`, {
                    httpOnly: true,
                    path: '/',
                    secure: true,
                    sameSite: 'strict',
                    maxAge: 60 * 60 * 24 // 1 day
                });


        } catch (_error) {
            throw error(500, {
                message: 'Something went wrong'
            });
        }

        throw redirect(302, '/');
    }
};