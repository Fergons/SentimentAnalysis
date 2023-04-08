from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import crud, schemas, models
import asyncio
import pytest
from app.services.analyzer.db_analyzer import analyze_db_reviews

pytestmark = pytest.mark.anyio


@pytest.fixture
async def seed_data(session: AsyncSession):
    # Create some sample data here
    game = models.Game(id=1, name="Test Game")
    source = models.Source(id=1, name="Test Source")
    reviewer = models.Reviewer(id=1, name="Test Reviewer")

    review1 = models.Review(id=1, source_review_id="1", text="This game is awesome! Gameplay is stellar!",
                            language="english", source_id=1,
                            game_id=1, reviewer_id=1)
    review2 = models.Review(id=2, source_review_id="2", text="I love this game! Gunplay is amazing.",
                            language="english", source_id=1,
                            game_id=1, reviewer_id=1)

    reviews = [review1, review2]
    for i in range(100):
        review = models.Review(id=i + 3, source_review_id=str(i + 3), text=f"Gameplay fun but visuals are trashy.",
                               language="english", source_id=1,
                               game_id=1, reviewer_id=1)
        reviews.append(review)

    session.add_all([game, source, reviewer, *reviews])
    await session.commit()

    return {"game": game, "source": source, "reviewer": reviewer, "review1": review1, "review2": review2,
            "reviews": reviews}


async def test_analyze_db_reviews(clear_db, session: AsyncSession, seed_data: dict):
    await analyze_db_reviews(session, game_id=seed_data["game"].id, task="joint-acos", model_name="mt5-acos-1.0")

    result = await session.execute(select(models.AnalyzedReview).where(
        models.AnalyzedReview.review_id.in_([seed_data["review1"].id, seed_data["review2"].id])))
    a_r = result.scalars().all()
    assert len(a_r) == 2
    assert a_r[0].review_id == seed_data["review1"].id and a_r[1].review_id == seed_data["review2"].id \
           or a_r[0].review_id == seed_data["review2"].id and a_r[1].review_id == seed_data["review1"].id

    if a_r[0].prediction != None:
        result = await session.execute(select(models.Review).where(models.Review.id == seed_data["review1"].id).options(
            selectinload(models.Review.aspects)))
        review1 = result.scalars().first()
        assert len(review1.aspects) > 0

    if a_r[0].prediction != None:
        result = await session.execute(select(models.Review).where(models.Review.id == seed_data["review2"].id).options(
            selectinload(models.Review.aspects)))
        review2 = result.scalars().first()
        assert len(review2.aspects) > 0


async def test_analyze_many_reviews_10_batch(clear_db, session: AsyncSession, seed_data: dict):
    await analyze_db_reviews(session, game_id=seed_data["game"].id, task="joint-acos", model_name="mt5-acos-1.0",
                             batch_size=10)
    result = await session.execute(select(models.AnalyzedReview))
    a_r = result.scalars().all()
    assert len(a_r) == len(seed_data["reviews"])


async def test_analyze_many_reviews_100_batch(clear_db, session: AsyncSession, seed_data: dict):
    await analyze_db_reviews(session, game_id=seed_data["game"].id, task="joint-acos", model_name="mt5-acos-1.0",
                             batch_size=100)
    result = await session.execute(select(models.AnalyzedReview))
    a_r = result.scalars().all()
    assert len(a_r) == len(seed_data["reviews"])
