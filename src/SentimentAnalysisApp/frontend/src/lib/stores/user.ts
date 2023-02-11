import {browser} from '$app/environment';
import {writable} from 'svelte/store';
import type {User} from "../client";

const defaultValue = null;
const initialValue = browser ? window.localStorage.getItem('user') ?? defaultValue : defaultValue;

const userStore = writable<User | null>(initialValue ? JSON.parse(initialValue) : null);

userStore.subscribe((value) => {
    if (browser) {
        window.localStorage.setItem('user', JSON.stringify(value));
    }
});

export default userStore;
