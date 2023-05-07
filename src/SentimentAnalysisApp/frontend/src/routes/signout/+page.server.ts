// Created by Frantisek Sabol
import {redirect} from "@sveltejs/kit";
import type { Actions } from "./$types";
import {OpenAPI} from "../../lib/client";

export const actions: Actions = {
    default: async ({request, cookies}) => {
        OpenAPI.TOKEN = undefined;
        cookies.set('access_token', '', {
            path: '/',
            expires: new Date(0),
        })
        throw redirect(301, '/signin');
    }
}