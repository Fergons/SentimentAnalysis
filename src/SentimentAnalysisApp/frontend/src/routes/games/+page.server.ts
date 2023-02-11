import { GamesService} from "../../lib/client";
import type {Game} from "../../lib/client";
import {error} from '@sveltejs/kit';

export async function load() {
    try {
        let games = new Map<number,Game>();
        const response = await GamesService.readGamesGamesGet();
        for (const {id, ...rest} of response) {
            games.set(id, {
                    id,
                    ...rest
                });
         }
        return {
            title: 'Games',
            games: games
        };
    } catch (err) {
        console.log(err);
        throw error(500, "Something went wrong.");
    }
}
