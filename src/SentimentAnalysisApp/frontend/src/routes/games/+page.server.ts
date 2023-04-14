import {error} from '@sveltejs/kit';
import {GamesService} from "../../lib/client";

export async function load() {
    try {
        return {
            name: 'Games',
            subtitle: ''
        };
    } catch (err) {
        console.log(err);
        throw error(500, "Something went wrong.");
    }
}
