// <!-- Created by Frantisek Sabol -->
import type {Handle} from '@sveltejs/kit';
import {OpenAPI, UsersService} from "./lib/client";
import {redirect} from "@sveltejs/kit";

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
            console.log("Error while getting current user: no user found or token expired.")
        } finally {
            OpenAPI.TOKEN = undefined;
        }
    }

    return resolve(event);
}