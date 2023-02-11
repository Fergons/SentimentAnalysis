import type {LayoutServerLoad} from "../../.svelte-kit/types/src/routes/$types";
import {redirect} from "@sveltejs/kit";
import type {Actions} from "@sveltejs/kit";
import userStore from "../lib/stores/user";

export const load: LayoutServerLoad = (event) => {
    console.log("Layout server load");
    return {
        token: event.locals.token
    }
};