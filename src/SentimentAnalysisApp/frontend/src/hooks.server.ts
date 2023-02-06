import {getUser} from "./lib/server/api/auth";
import type {Handle} from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').Handle} */

export let handle: Handle = async function ({event, resolve}) {
    const token = event.cookies.get('access_token');
    if (!token) {
        event.locals.token = null;
        event.locals.authenticated = false;
    }else{
        event.locals.token = token;
        event.locals.authenticated = true;
    }
      return resolve(event);
}