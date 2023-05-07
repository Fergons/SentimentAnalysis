// Created by Frantisek Sabol
import {z} from 'zod';
import type {PageServerLoad, Actions} from './$types';
import {redirect, error} from '@sveltejs/kit';
import {validateFormData} from "../../lib/utils/validation";
import type {User, UserCreate} from "../../lib/client";
import {ApiError, AuthService, UsersService} from "../../lib/client";

export const load: PageServerLoad = (event) => {
    if (event.locals.token) {
        throw redirect(301, '/');
    }
};

const signupSchema = z
    .object({
        email: z
            .string({required_error: 'Email is required'})
            .min(1, {message: 'Email is required'})
            .max(64, {message: 'Email must be less than 64 characters long'})
            .email({message: 'Email must be a valid email address'}),
        password: z
            .string({required_error: 'Password is required'})
            .min(8, {message: 'Password must be at least 8 characters long'})
            .max(32, {message: 'Password must be less than 32 characters long'})
            .trim(),
        passwordConfirm: z
            .string({required_error: 'Password is required'})
            .min(6, {message: 'Password must be at least 6 characters'})
            .max(32, {message: 'Password must be less than 32 characters'})
            .trim(),
    })
    .superRefine(({passwordConfirm, password}, ctx) => {
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
        const formData = Object.fromEntries(await request.formData()) as unknown as UserCreate;
        const validation = validateFormData<UserCreate>(formData, signupSchema);
        if (!validation.success) {
            return {
                errors: validation.errors,
            }
        }
        try {
            const response = await AuthService.registerRegisterAuthRegisterPost(formData);
            return {
                ...response
            }
        } catch (e: any) {
            if (e.name && e.name === 'ApiError'){
                return {
                    email: formData.email,
                    errors: {
                        ...e.request.errors
                    }
                }
            }
            throw error(e);
        }
    }
};

