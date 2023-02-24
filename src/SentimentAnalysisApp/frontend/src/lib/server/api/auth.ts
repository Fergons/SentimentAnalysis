import {handleApiResponseError} from './api';
import {z} from 'zod';

export const SigninSchema = z.object({
    username: z
        .string({required_error: 'Email is required'})
        .min(1, {message: 'Email is required'})
        .max(64, {message: 'Email must be less than 64 characters long'})
        .email({message: 'Email must be a valid email address'}),

    password: z
        .string({required_error: 'Password is required'})
        .min(1, {message: 'Password is required'})
        .max(32, {message: 'Password must be less than 32 characters long'})
});

export type SigninDataType = z.infer<typeof SigninSchema>;

export type SigninResponse = {
    access_token: string
};