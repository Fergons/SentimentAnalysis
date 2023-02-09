import {getAccountDetail} from "./lib/server/api/auth";
import {get} from "svelte/store";
import type {Handle} from '@sveltejs/kit';
import userStore from './lib/stores/user';
import type {User} from "./lib/server/api/types";

/** @type {import('@sveltejs/kit').Handle} */

export let handle: Handle = async function ({event, resolve}) {
    const token = event.cookies.get('access_token');
    if (!token) {
        userStore.set(null);
    }else if (!event.locals.user) {
        if(get(userStore) === null){
            const user = await getAccountDetail<User>(token);
            userStore.set(user);
            event.locals.user = user;
        }else{
            event.locals.user = get(userStore);
        }
    }
      return resolve(event);
}