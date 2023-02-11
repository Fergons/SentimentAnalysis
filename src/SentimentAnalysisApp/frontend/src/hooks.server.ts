import {getAccountDetail} from "./lib/server/api/auth";
import {get} from "svelte/store";
import type {Handle} from '@sveltejs/kit';
import type {User} from "./lib/client";
import {OpenAPI, UsersService} from "./lib/client";

/** @type {import('@sveltejs/kit').Handle} */

export let handle: Handle = async function ({event, resolve}) {
    const token = event.cookies.get('access_token');
    if (token) {
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