import {error} from '@sveltejs/kit';
import {GamesService, ReviewsService} from "../../../lib/client";

export async function load({params}: { params: { id: number } }) {

    try {
        const [game, reviews_summary] = await Promise.all([
            GamesService.readGameGamesIdGet(params.id),
            ReviewsService.getSummaryReviewsSummaryGet(params.id)
        ]);

        return {
            title: game.name,
            subtitle: 'Overview',
            game: game,
            overview: {
                category_scores: new Map<string, number>([
                    ['price', 5],
                    ['story', 5],
                    ['community', 5],
                    ['gameplay', 1],
                    ['audio_visuals', 3],
                    ['performance_bugs', 9]
                ])
            },
            stats: {
                reviews_summary: reviews_summary
            }
        }


    } catch (e) {
        console.log(e);
        throw error(500, 'Api didn\'t respond');
    }

}
