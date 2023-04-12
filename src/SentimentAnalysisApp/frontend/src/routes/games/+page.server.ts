import { GamesService} from "../../lib/client";
import type {GameListItem} from "../../lib/client";
import {error} from '@sveltejs/kit';

export async function load() {
    try {
        let games = new Map<number, GameListItem>();
        const response = await GamesService.readGamesGamesGet(100,undefined, {
            name: 'counter-strike',
        });
        console.log(response)
        // @ts-ignore
        response.games.forEach((item: GameListItem) => {
            games.set(item.game.id, item);
        });

        return {
            title: 'Games',
            games: games,
            cursor: response.cursor
        };
    } catch (err) {
        console.log(err);
        throw error(500, "Something went wrong.");
    }
}
