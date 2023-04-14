import type {Handle} from '@sveltejs/kit';
import {OpenAPI, UsersService} from "./lib/client";

export let handle: Handle = async function ({event, resolve}) {
    const token = event.cookies.get('access_token');
    if (token) {
        event.locals.token = token;
    }
    if (event.url.pathname.startsWith('/users/me') ||
        event.url.pathname.startsWith('/signin') ||
        event.url.pathname.startsWith('/signup') ||
        event.url.pathname.startsWith('/signout')) {
        try {
            OpenAPI.TOKEN = token;
            event.locals.user = await UsersService.usersCurrentUserUsersMeGet();
        } catch (e){
            event.locals.token = undefined;
            console.log(e)
        } finally {
            OpenAPI.TOKEN = undefined;
        }
    }

    return resolve(event);
}