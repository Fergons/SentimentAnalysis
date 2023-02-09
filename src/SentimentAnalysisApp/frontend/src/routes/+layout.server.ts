import type {LayoutServerLoad} from "../../.svelte-kit/types/src/routes/$types";
import {redirect} from "@sveltejs/kit";
import userStore from "../lib/stores/user";

export const load: LayoutServerLoad = (event) => {
    userStore.set(event.locals.user);
    return {
        user: event.locals.user
    }
};