import asyncio
import json
from typing import List
from app.crud.review import crud_review
from app.db.session import async_session
from app.models.review import Review
from .analyze import get_extractor, extract_aspects
from .utils import clean


def analyze_db_review_bulk(reviews: List[Review]):
    """clean review.text, sentence tokenize review.text, analyze and return list of aspects"""
    result = {}
    extractor = get_extractor()
    for review in reviews:
        result[review.id] = extract_aspects(review.text, language=review.language, extractor=extractor)
    return result


async def analyze_db_reviews(db_session):
    reviews = await crud_review.get_not_processed_by_source(db_session, source_id=1, limit=10)
    result = analyze_db_review_bulk(reviews)
    print(result)


# async def clean_db_reviews(db_session):
#     reviews = await crud_review.get_not_processed_by_source(db_session, source_id=1, limit=10)
#     for review in reviews:
#         review.text = review.text.replace("")


# async def language_check(db_session):
#     reviews = await crud_review.get_not_processed_by_source(db_session, source_id=1, limit=10)
#     for review in reviews:
#         print(review.language)

async def dump_all_analyzed_reviews_to_file(db_session):
    reviews = await crud_review.get_with_aspects(db_session)
    with open("./reviews/review_id_text_aspects.txt", "w", encoding="utf-8") as f:
        for review in reviews:
            aspect_list = [
                {
                    "term": aspect.term,
                    "polarity": aspect.polarity,
                    "category": aspect.category
                } for aspect in review.aspects
            ]
            aspect_string = json.dumps(aspect_list, ensure_ascii=False)
            f.write(f"{review.id}\t{review.text}\t{aspect_string}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(analyze_db_reviews())
