import {error} from '@sveltejs/kit';
import {GamesService, ReviewsService, SourcesService} from "../../../lib/client";
import type {Game, ReviewsSummary, ReviewsSummaryDataPoint, Source} from "../../../lib/client";
import {getTotal} from "../../../lib/utils/dataTransformer";

export async function load({params}: { params: { id: number } }) {

    try {
        const [game, reviewsSummary, sources, aspectsSummary] = await Promise.all([
            GamesService.readGameGamesIdGet(params.id),
            GamesService.getSummaryV2GamesIdSummaryV2TimeIntervalGet(params.id, 'day'),
            GamesService.getSourcesGamesIdSourcesGet(params.id),
            GamesService.getAspectSummaryGamesIdSummaryAspectsGet(params.id)
        ]);

        const sourceMap = sources && sources.length ? sources.reduce((acc, obj: Source) => {
                acc.set(obj.id, obj);
                return acc;
            },
            new Map<number, Source>()) : new Map<number, Source>();

        return {
            name: game.name,
            subtitle: 'Overview',
            game: game,
            overview: {
                summary: aspectsSummary
            },
            stats: {
                summary: reviewsSummary,
                sources: sourceMap
            },

        }
    } catch (e) {
        console.log(e);
        throw error(500, 'Api didn\'t respond');
    }
}