import { z } from 'zod';
import type {PageServerLoad, Actions} from './$types';
import {redirect, error} from '@sveltejs/kit';
import {handleApiResponseError} from "../../lib/server/api/api";
import {signup} from '../../lib/server/api/auth';
import type {SigninDataType} from '../../lib/server/api/auth';
import {SigninSchema} from '../../lib/server/api/auth';
import {api} from '../../lib/server/api/api';
import {validateFormData} from "../../lib/utils/validation";

export const load: PageServerLoad = (event) => {
    if (event.locals.user) {
        throw redirect(302, '/');
    }
};

const signupSchema = z
	.object({
		email: z
			.string({ required_error: 'Email is required' })
			.min(1, { message: 'Email is required' })
			.max(64, { message: 'Email must be less than 64 characters long' })
			.email({ message: 'Email must be a valid email address' }),
		password: z
			.string({ required_error: 'Password is required' })
			.min(8, { message: 'Password must be at least 8 characters long' })
			.max(32, { message: 'Password must be less than 32 characters long' })
			.trim(),
		passwordConfirm: z
			.string({ required_error: 'Password is required' })
			.min(6, { message: 'Password must be at least 6 characters' })
			.max(32, { message: 'Password must be less than 32 characters' })
			.trim(),
	})
	.superRefine(({ passwordConfirm, password }, ctx) => {
		if (passwordConfirm !== password) {
			ctx.addIssue({
				code: 'custom',
				message: 'Password and Confirm Password must match',
				path: ['password']
			});
			ctx.addIssue({
				code: 'custom',
				message: 'Password and Confirm Password must match',
				path: ['passwordConfirm']
			});
		}
	});

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
            const response = await signup(formData.email, formData.password);
            if (response.email !== formData.email) {
                return {
                    data: {
                        email: formData.email
                    },
                    errors: {
                        response: {status: 500, message: "Unexpected response from server."}
                    }
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
        throw redirect(302, '/signin');
    }
};

