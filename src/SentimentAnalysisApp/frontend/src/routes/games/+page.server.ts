import {getGames} from '../../lib/server/api/games';
import {error} from '@sveltejs/kit';

export async function load() {

    const games = await getGames();
    return {
        title: 'Games',
        games: games
    };
}
