import type { PageLoad } from './$types'
import type {Review, ReviewWithAspects} from "../../lib/client";
import {ReviewsService} from "../../lib/client";

const review: ReviewWithAspects = {
        id: 1,
        language: 'czech',
        text: 'This is a review about a game. Because of Aspect_1 I think the game is bad.',
        aspects: [
            {
                id: 1,
                term: 'Aspect_1',
                polarity: 'negative',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 2,
                term: 'Aspect_2',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 3,
                term: 'Aspect_3',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 4,
                term: 'Aspect_4',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 5,
                term: 'Aspect_5',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 6,
                term: 'Aspect_6',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 7,
                term: 'Aspect_7',
                polarity: 'positive',
                category: 'audio_visual',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 8,
                term: 'Aspect_8',
                polarity: 'positive',
                category: 'price',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 9,
                term: 'Aspect_9',
                polarity: 'positive',
                category: 'story',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 10,
                term: 'Aspect_10',
                polarity: 'positive',
                category: 'community',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 11,
                term: 'Aspect_11',
                polarity: 'positive',
                category: 'community',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 12,
                term: 'Aspect_12',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            },
            {
                id: 13,
                term: 'Aspect_13',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4",
                updated_at: "2021-05-01T00:00:00.000Z"
            }
        ]
    };

export async function load() {
    let reviews = new Map<number,ReviewWithAspects>();
    const response: ReviewWithAspects[] =  [review]//await ReviewsService.readProcessedReviewsReviewsProcessedGet();
    for (const review of response) {
        reviews.set(review.id, review);
    }
    return {
        title: 'Reviews',
        reviews: reviews
    }
}