import {error} from '@sveltejs/kit';
import {getGame} from '../../../lib/server/api/games';
import type {Game} from '../../../lib/server/api/types';

export async function load({params}: { params: { id: string } }) {

    let game = await getGame(params.id);
    if (game) {
        return {
            title: game.name,
            subtitle: 'Overview',
            game: game
        };
    }
    throw error(404, 'Not found');


}
