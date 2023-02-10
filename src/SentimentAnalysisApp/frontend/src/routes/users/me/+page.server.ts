import type {PageServerLoad} from "./$types";
import {redirect} from "@sveltejs/kit";
import type {Actions} from "./$types";
import {validateFormData} from "../../../lib/utils/validation";
import {api, handleApiResponseError} from "../../../lib/server/api/api";
import {z} from "zod";

const updateUserSchema = z.object({
    email: z.string().email().trim()
});
export const load: PageServerLoad = async (event) => {
    if (!event.locals.user) {
        throw redirect(302, '/signin');
    } else {
        return {
            user: event.locals.user
        }
    }
};

export const actions: Actions = {
    default: async ({request}) => {
        const formData = Object.fromEntries(await request.formData()) as { email: string };
        const validation = validateFormData<{ email: string }>(formData, updateUserSchema);
        if (!validation.success) {
            return {
                errors: validation.errors,
            }
        }
        console.log(formData)
        try {
            // const response = await userUpdate(formData.email);
            const response = {email: formData.email}
            return {
                data: {
                    ...response
                }
            }
        } catch (e) {
            const response = handleApiResponseError(e);
            return {
                data: {
                    email: formData.email
                },
                errors: {
                    response: response
                }
            }
        }
    }
}