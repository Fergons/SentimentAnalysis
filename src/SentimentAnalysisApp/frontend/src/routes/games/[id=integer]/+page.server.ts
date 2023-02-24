import {error} from '@sveltejs/kit';
import {GamesService} from "../../../lib/client";

export async function load({params}: { params: { id: number } }) {

    let game = await GamesService.readGameGamesIdGet(params.id);
    if (game) {
        return {
            title: game.name,
            subtitle: 'Overview',
            game: game,
            category_scores: new Map<string, number>([
                ['price', 5],
                ['story', 5],
                ['community', 5],
                ['gameplay', 1],
                ['audio_visuals',3],
                ['performance_bugs', 9]
            ])
        }
    }
    throw error(404, 'Not found');
}
