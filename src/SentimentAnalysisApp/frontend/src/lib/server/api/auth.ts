import { api } from './api';
export async function signin(email: string, password: string) {
  try {
    const response = await api.post('/auth/jwt/login', {
      username: email,
      password: password,
    });
    if(response.data.access_token!==undefined)
        return response.data.access_token;
    else{
        console.error(response.data.detail);
        return null;
    }

  } catch (error) {
    throw error;
  }
}

export async function getUser(jwt: string) {
    try {
        const response = await api.get('/users/me', {
        headers: {
            Authorization: jwt,
        },
        });
        return response.data;
    } catch (error) {
        console.error(error);
        return null;
    }
}

export async function signout() {

}

export async function signup(email: string, password: string) {

}