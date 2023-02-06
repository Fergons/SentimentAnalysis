import { api } from './api';
export async function signin(email: string, password: string) {
  try {
    const response = await api.post('/auth/jwt/login', {
      username: email,
      password: password,
    });
      return response.data.access_token;

  } catch (error) {
    console.error(error);
    return error;
  }
}

export async function signout() {

}

export async function signup(email: string, password: string) {

}