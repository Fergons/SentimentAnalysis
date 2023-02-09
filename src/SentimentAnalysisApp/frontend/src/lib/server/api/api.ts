import axios, {isAxiosError} from 'axios';
import type {HttpError} from "@sveltejs/kit";

const API_URL = 'http://127.0.0.1:8000/';

export const api = axios.create({
    baseURL: API_URL,
    timeout: 1000,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'FrontendApp'
    },
});

export function handleApiResponseError(err: any): HttpError {
    if (isAxiosError(err)) {
        if (err.response) {
            console.log(err.response.data)
            return {
                body: {message: err.response.data?.detail},
                status: err.response.status
            };
        } else if (err.request) {
            return {
                body: {message:  `Unable to establish connection to ${err.config?.url}`},
                status: 500
            };
        }
    }
    console.log(err)
    return {
        body: {message: "WTF"},
        status: 500
    };
}


