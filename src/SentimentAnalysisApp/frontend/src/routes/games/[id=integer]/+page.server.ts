import {error} from '@sveltejs/kit';
import {GamesService, ReviewsService, SourcesService} from "../../../lib/client";
import type {Game, ReviewsSummary, ReviewsSummaryDataPoint, Source} from "../../../lib/client";
import {getTotal} from "../../../lib/utils/dataTransformer";

export async function load({params}: { params: { id: number } }) {

    try {
        const [game, reviews_summary, sources] = await Promise.all([
            GamesService.readGameGamesIdGet(params.id),
            ReviewsService.getSummaryReviewsSummaryGet(params.id),
            SourcesService.readSourcesSourcesGet()
        ]);
        const sourceMap = sources.reduce((acc, obj: Source) => {
                acc.set(obj.id, obj);
                return acc;
            },
            new Map<number, Source>())

        return {
            title: game.name,
            subtitle: 'Overview',
            game: game,
            overview: {
                categories: [
                    {
                        game_id: game.id,
                        price: 5,
                        story: 5,
                        community: 5,
                        gameplay: 1,
                        audio_visuals: 3,
                        performance_bugs: 9
                    }
                ]

            },
            stats: {
                total: getTotal(reviews_summary.data ?? [] as ReviewsSummaryDataPoint[], sourceMap),
                total_flat: reviews_summary.data ?? [] as ReviewsSummaryDataPoint[],
                sources: sourceMap
            },

        }
    } catch (e) {
        console.log(e);
        throw error(500, 'Api didn\'t respond');
    }

}
