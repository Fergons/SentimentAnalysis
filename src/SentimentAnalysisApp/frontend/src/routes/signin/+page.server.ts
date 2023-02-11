import type {PageServerLoad, Actions} from './$types';
import {redirect, error} from '@sveltejs/kit';
import {handleApiResponseError} from "../../lib/server/api/api";
import {getAccountDetail, signin} from '../../lib/server/api/auth';
import type {SigninDataType} from '../../lib/server/api/auth';
import {SigninSchema} from '../../lib/server/api/auth';
import {validateFormData} from "../../lib/utils/validation";
import {invalidateAll} from "$app/navigation";
import type {User} from "../../lib/shared/types";
import {AuthService, OpenAPI, UsersService} from "../../lib/client";
import type {Body_auth_jwt_login_auth_jwt_login_post} from "../../lib/client";

export const load: PageServerLoad = (event) => {
    if (event.locals.token) {
        throw redirect(301, '/');
    }
};


export const actions: Actions = {
    default: async ({request, cookies}) => {
        const formData = Object.fromEntries(await request.formData()) as Body_auth_jwt_login_auth_jwt_login_post;
        const validation = validateFormData<Body_auth_jwt_login_auth_jwt_login_post>(formData, SigninSchema);
        if (!validation.success) {
            return {
                errors: validation.errors,
            }
        }
        try {
            const response = await AuthService.authJwtLoginAuthJwtLoginPost(formData);
            if (response.access_token === undefined) {
                return {
                    email: formData.username,
                    errors: {
                        response: {status: 500, message: "Unexpected response from server."}
                    }
                }
            }
            // OpenAPI.TOKEN = response.access_token;
            // const user = await UsersService.usersCurrentUserUsersMeGet();

            cookies.set('access_token', `${response.access_token}`, {
                httpOnly: true,
                path: '/',
                secure: true,
                sameSite: 'strict',
                maxAge: 60 * 60 * 24 // 1 day
            });

            return {
                token: response.access_token,
            }


        } catch (e) {
            const response = handleApiResponseError(e);
            return {
                email: formData.username,
                errors: {
                    response: response
                }
            }
        }
    }
};