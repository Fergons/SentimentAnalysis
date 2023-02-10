import {getAccountDetail} from "./lib/server/api/auth";
import {get} from "svelte/store";
import type {Handle} from '@sveltejs/kit';
import type {User} from "./lib/shared/types";

/** @type {import('@sveltejs/kit').Handle} */

export let handle: Handle = async function ({event, resolve}) {
    const token = event.cookies.get('access_token');
    if (!token) {
        event.locals.user = null;
    }else if (!event.locals.user) {
        console.log(event.url.pathname, event.locals.user);
        if(event.url.pathname !== "/signout"){

            event.locals.user = await getAccountDetail<User>(token);
            console.log("User details received: " + JSON.stringify(event.locals.user));
        }
    }
    return resolve(event);
}