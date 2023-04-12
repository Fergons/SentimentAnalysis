import {error} from '@sveltejs/kit';
import {GamesService, ReviewsService, SourcesService} from "../../../lib/client";
import type {Game, ReviewsSummary, ReviewsSummaryDataPoint, Source} from "../../../lib/client";
import {getTotal} from "../../../lib/utils/dataTransformer";

export async function load({params}: { params: { id: number } }) {

    try {
        const [game, reviews_summary, sources] = await Promise.all([
            GamesService.readGameGamesIdGet(params.id),
            GamesService.getSummaryV2GamesIdSummaryV2TimeIntervalGet(params.id, 'day'),
            GamesService.getSourcesGamesIdSourcesGet(params.id)
        ]);

        const sourceMap = sources && sources.length ? sources.reduce((acc, obj: Source) => {
                acc.set(obj.id, obj);
                return acc;
            },
            new Map<number, Source>()) : new Map<number, Source>();

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
                summary: reviews_summary,
                sources: sourceMap
            },

        }
    } catch (e) {
        console.log(e);
        throw error(500, 'Api didn\'t respond');
    }
}

