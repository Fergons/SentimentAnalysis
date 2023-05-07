// Created by Frantisek Sabol
import type {PageServerLoad} from "./$types";
import {redirect} from "@sveltejs/kit";
import type {Actions} from "./$types";
import {validateFormData} from "../../../lib/utils/validation";
import {handleApiResponseError} from "../../../lib/server/api/api";
import {z} from "zod";
import {OpenAPI, UsersService} from "../../../lib/client";
import type {User, UserUpdate} from "../../../lib/client";


const updateUserSchema = z.object({
    email: z.string().email().trim()
});
export const load: PageServerLoad = async (event) => {
    if (!event.locals.token) {
        throw redirect(302, '/signin');
    } else {
        return {
            token: event.locals.token,
            user: event.locals.user
        }
    }
};

export const actions: Actions = {
    default: async ({request,locals}) => {
        const formData = Object.fromEntries(await request.formData()) as UserUpdate;
        const validation = validateFormData<UserUpdate>(formData, updateUserSchema);
        if (!validation.success) {
            return {
                errors: validation.errors,
            }
        }
        console.log(formData)
        try {
            OpenAPI.TOKEN = locals.token;
            if(locals.user?.id){
                const response = await UsersService.usersUserUsersIdPatch(locals.user.id, formData);
                return {
                    ...response
                }
            }
        } catch (e) {
            const response = handleApiResponseError(e);
            return {
                email: formData.email,
                errors: {
                    response: response
                }
            }
        } finally {
             OpenAPI.TOKEN = undefined;
        }
    }
}