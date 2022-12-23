import asyncio
from typing import List
from app.crud.review import crud_review
from app.db.session import async_session
from app.models.review import Review
from .analyze import get_extractor, extract_aspects


def analyze_db_review_bulk(reviews: List[Review]):
    """clean review.text, sentence tokenize review.text, analyze and return list of aspects"""
    result = {}
    extractor = get_extractor()
    for review in reviews:
        result[review.id] = extract_aspects(review.text, language=review.language, extractor=extractor)
    return result


async def analyze_db_reviews():
    async with async_session() as session:
        reviews = await crud_review.get_not_processed_by_source(session, source_id=1, limit=10)

    result = analyze_db_review_bulk(reviews)
    print(result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(analyze_db_reviews())