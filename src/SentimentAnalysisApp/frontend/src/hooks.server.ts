import type {Handle} from '@sveltejs/kit';
import {OpenAPI, UsersService} from "./lib/client";

export let handle: Handle = async function ({event, resolve}) {
    const token = event.cookies.get('access_token');
    if (token) {
        console.log("Token found");
        event.locals.token = token;
    }
    if (event.url.pathname.startsWith('/users/me')) {
        try {
            OpenAPI.TOKEN = token;
            event.locals.user = await UsersService.usersCurrentUserUsersMeGet();
        } catch (e){
            console.log(e)
        } finally {
            OpenAPI.TOKEN = undefined;
        }
    }
    return resolve(event);
}