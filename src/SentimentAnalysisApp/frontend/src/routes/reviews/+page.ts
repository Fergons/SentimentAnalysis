import type { PageLoad } from './$types'
import type {Review, ReviewWithAspects} from "../../lib/client";
import {ReviewsService} from "../../lib/client";

export async function load() {
    let reviews = new Map<number,ReviewWithAspects>();
    const response: ReviewWithAspects[] = await ReviewsService.readProcessedReviewsReviewsProcessedGet();
    for (const review of response) {
        reviews.set(review.id, review);
    }
    return {
        title: 'Reviews',
        reviews: reviews
    }
}