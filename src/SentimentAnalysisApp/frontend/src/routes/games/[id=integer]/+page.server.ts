import {error} from '@sveltejs/kit';
import {getGame} from '../../../lib/server/api/games';
import type {Game} from '../../../lib/client';

export async function load({params}: { params: { id: string } }) {

    let game = await getGame(params.id);
    if (game) {
        return {
            title: game.name,
            subtitle: 'Overview',
            game: game,
            category_scores: new Map<string, number>([
                ['price', 0.5],
                ['story', 0.5],
                ['community', 0.5],
                ['gameplay', 0.5],
                ['audio_visuals', 0.5],
                ['performance_bugs', 0.5]
            ])
        }
    }
    throw error(404, 'Not found');
}
