import type {PageServerLoad, Actions} from './$types';
import {redirect, error} from '@sveltejs/kit';
import {handleApiResponseError} from "../../lib/server/api/api";
import {getAccountDetail, signin} from '../../lib/server/api/auth';
import type {SigninDataType} from '../../lib/server/api/auth';
import {SigninSchema} from '../../lib/server/api/auth';
import {api} from '../../lib/server/api/api';
import {validateFormData} from "../../lib/utils/validation";
import {invalidateAll} from "$app/navigation";
import type {User} from "../../lib/shared/types";
import * as wasi from "wasi";


export const load: PageServerLoad = (event) => {
    if (event.locals.user) {
        throw redirect(302, '/');
    }
};


export const actions: Actions = {
    default: async ({request, cookies}) => {
        const formData = Object.fromEntries(await request.formData()) as SigninDataType;
        const validation = validateFormData<SigninDataType>(formData, SigninSchema);
        if (!validation.success) {
            return {
                errors: validation.errors,
            }
        }
        try {
            const response = await signin(formData.email, formData.password);
            if (response.access_token === undefined) {
                return {
                    data: {
                        email: formData.email
                    },
                    errors: {
                        response: {status: 500, message: "Unexpected response from server."}
                    }
                }
            }
            cookies.set('access_token', `Bearer ${response.access_token}`, {
                httpOnly: true,
                path: '/',
                secure: true,
                sameSite: 'strict',
                maxAge: 60 * 60 * 24 // 1 day
            });

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
        throw redirect(302, '/');
    }
};