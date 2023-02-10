import {redirect} from "@sveltejs/kit";
import type { Actions } from "./$types";

export const actions: Actions = {
    default: async ({request, cookies}) => {
        cookies.set('access_token', '', {
            path: '/',
            expires: new Date(0),
        })
        throw redirect(302, '/signin');
    }
}