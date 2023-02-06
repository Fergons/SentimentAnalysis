import type {PageServerLoad} from "./$types";
import {redirect} from "@sveltejs/kit";
import {getUser} from "../../../lib/server/api/auth";


export const load: PageServerLoad = async (event) => {
    if (!event.locals.authenticated) {
        throw redirect(302, '/signin');
    }
    else{
        const user = await getUser(event.locals.token);
        if(!user.email){
             //TODO: push snackbar to kitchen
            throw redirect(302, '/signin');
        }
        console.log(user);
        return {
            user: user
        }
    }
};