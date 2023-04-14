import type {PageLoad} from './$types'
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
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z",
            review_id: 1,
            model_id: "v1"
        },
        {
            id: 2,
            term: 'Aspect_2',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z",
            review_id: 1,
            model_id: "v1"
        },
        {
            id: 3,
            term: 'Aspect_3',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z",
            review_id: 1,
            model_id: "v1"
        },
        {
            id: 4,
            term: 'Aspect_4',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z",
            review_id: 1,
            model_id: "v1"
        },
        {
            id: 5,
            term: 'Aspect_5',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 6,
            term: 'Aspect_6',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 7,
            term: 'Aspect_7',
            polarity: 'positive',
            category: 'audio_visual',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 8,
            term: 'Aspect_8',
            polarity: 'positive',
            category: 'price',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 9,
            term: 'Aspect_9',
            polarity: 'positive',
            category: 'story',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 10,
            term: 'Aspect_10',
            polarity: 'positive',
            category: 'community',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 11,
            term: 'Aspect_11',
            polarity: 'positive',
            category: 'community',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 12,
            term: 'Aspect_12',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        },
        {
            id: 13,
            term: 'Aspect_13',
            polarity: 'positive',
            category: 'gameplay',
            opinion: "0.4",
            updated_at: "2021-05-01T00:00:00.000Z", review_id: 1,
            model_id: "v1"
        }
    ]
};

export async function load() {
    let reviews = new Map<number, ReviewWithAspects>();
    const response: ReviewWithAspects[] = [review]//await ReviewsService.readProcessedReviewsReviewsProcessedGet();
    for (const review of response) {
        reviews.set(review.id, review);
    }
    return {
        title: 'Reviews',
        reviews: reviews
    }
}