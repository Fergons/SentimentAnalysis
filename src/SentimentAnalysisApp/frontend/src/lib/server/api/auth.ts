import {api, handleApiResponseError} from './api';
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
export async function signin(email: string, password: string): Promise<SigninResponse> {

    const response = await api.post('/auth/jwt/login', {
        username: email,
        password: password,
    });
    return response.data;
}

type AccountDetailResponse = {
    id: number;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
}

export async function getAccountDetail<ResultType = Record<string, any>>(jwt: string): Promise<ResultType | null> {
    try {
        const response = await api.get('/users/me', {
            headers: {
                Authorization: jwt,
            },
        });
        return response.data;
    } catch (e){
        return null
    }

}

export async function signout() {

}

export async function signup(email: string, password: string) {
    const response = await api.post('/auth/register/', {
        email: email,
        password: password
    });
    return response.data;
}