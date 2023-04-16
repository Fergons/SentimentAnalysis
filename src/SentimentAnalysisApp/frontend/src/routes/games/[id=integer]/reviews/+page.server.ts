import type { PageServerLoad } from './$types';
import type { ReviewListResponse, Source} from '../../../../lib/client';
import {ReviewsService, SourcesService} from "../../../../lib/client";

const aspects = ['overall', 'gameplay', 'performance_bugs', 'price', 'audio_visuals', 'community'];
const polarities = ['positive', 'negative', 'neutral'];
export const load = (async ({ params, url }) => {
    const gameId = Number(params.id) || undefined;
    let page = Number(url.searchParams.get('page'))-1 || 0;
    page = page < 0 ? 0 : page;
    const pageSize = Number(url.searchParams.get('limit')) || 20;
    const offset = page * pageSize;
    const source = Number(url.searchParams.get('source')) || undefined;
    const aspect = url.searchParams.get('aspect') || undefined;
    const processed = Boolean(url.searchParams.get('processed'))|| true;
    try{
        return {
            subtitle: 'Reviews',
            reviews: ReviewsService.readReviewsReviewsGet(gameId, source, processed, offset, 100),
            sources: SourcesService.readSourcesSourcesGet(),
            aspects: aspects,
            polarities: polarities,
        }

    }catch (e) {
        console.log(e);
        return {
            subtitle: 'Reviews',
            reviews: [],
            total: 0,
            sources: [],
            aspects: aspects,
        };
    }
}) as PageServerLoad;
