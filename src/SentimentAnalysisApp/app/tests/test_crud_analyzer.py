from datetime import datetime
import random

import pytest
import httpx
import respx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.orm import selectinload
from app import crud, schemas, models
import asyncio
pytestmark = pytest.mark.anyio

@pytest.fixture
async def review(session: AsyncSession):
    # insert a review into the database
    review = models.Review(
        id=1,
        text="This is a test review about great gameplay and such. Graphics are great too. :DDDDDD",
        language="english"
    )
    session.add(review)
    await session.commit()
    return review

@pytest.fixture
async def analyzed_review(session: AsyncSession, review: models.Review):
    # insert an analyzed review into the database
    analyzed_review = models.AnalyzedReview(
        review_id=review.id,
        cleaned_text="This is a test review about great gameplay and such. Graphics are not great.",
        model="test_model",
        prediction="positive",
        gold_label="positive",
        created_at=datetime.now()
    )
    session.add(analyzed_review)
    await session.commit()
    return analyzed_review


# conftest.py

@pytest.fixture
async def seeded_data(session: AsyncSession):
    # Seed the data
    source = models.Source(id=1, name="test_source")
    game = models.Game(id=1, name="test_game", release_date=datetime.now())

    reviews_data = [
        (1, "1", "test_review1", "english", 1, 1),
        (2, "2", "test_review2", "english", 1, 1),
        (3, "3", "test_review3", "english", 1, 1),
        (4, "4", "test_review4", "english", 1, 1),
    ]

    analyzed_reviews_data = [
        (1, 1, "task1", "model1", "positive", "positive"),
        (2, 2, "task1", "model1", "negative", "negative"),
        (3, 3, "task1", "model1", "neutral", "neutral"),
        (4, 4, "task1", "model1", "positive", "positive"),
    ]

    analyzed_sentences_data = [
        (1, 1, "Test sentence 1", "positive", "positive"),
        (2, 2, "Test sentence 2", "negative", "negative"),
        (3, 3, "Test sentence 3", "neutral", "neutral"),
        (4, 4, "Test sentence 4", "positive", "positive"),
    ]

    reviews = [
        models.Review(id=id_, source_review_id=source_review_id, text=text, language=language, source_id=source_id,
                      game_id=game_id)
        for id_, source_review_id, text, language, source_id, game_id in reviews_data]
    analyzed_reviews = [
        models.AnalyzedReview(id=id_, review_id=review_id, task=task, model=model, prediction=prediction,
                              gold_label=gold_label)
        for id_, review_id, task, model, prediction, gold_label in analyzed_reviews_data]
    analyzed_sentences = [
        models.AnalyzedReviewSentence(id=id_, analyzed_review_id=analyzed_review_id, sentence=sentence,
                                      prediction=prediction, gold_label=gold_label)
        for id_, analyzed_review_id, sentence, prediction, gold_label in analyzed_sentences_data]

    session.add_all([source, game] + reviews + analyzed_reviews + analyzed_sentences)
    await session.commit()


async def test_create_analyzed_review(clear_db, session: AsyncSession, review: models.Review):
    analyzed_review = await crud.analyzed_review.create(session, obj_in=schemas.AnalyzedReviewCreate(
        review_id=review.id,
        cleaned_text="This is a test review about great gameplay and such. Graphics are not great.",
        model="test_model",
        prediction="positive",
        gold_label="positive",
        created_at=datetime.now()))

    result = await session.execute(select(models.AnalyzedReview).where(models.AnalyzedReview.id == analyzed_review.id))
    analyzed_review = result.scalars().first()
    assert analyzed_review.review_id == review.id
    assert analyzed_review.cleaned_text == "This is a test review about great gameplay and such. Graphics are not great."
    assert analyzed_review.model == "test_model"
    assert analyzed_review.prediction == "positive"
    assert analyzed_review.gold_label == "positive"
    assert analyzed_review.created_at is not None
    return analyzed_review


@pytest.mark.asyncio
async def test_create_analyzed_review_sentence(
        clear_db, session: AsyncSession, review: models.Review, analyzed_review: models.AnalyzedReview):
    sentence1 = await crud.analyzed_review_sentence.create(session, obj_in=schemas.AnalyzedReviewSentenceCreate(
        sentence="This is a test review about great gameplay and such.",
        prediction="positive",
        gold_label="positive",
        analyzed_review_id=analyzed_review.id,
        created_at=datetime.now()))

    sentence2 = await crud.analyzed_review_sentence.create(session, obj_in=schemas.AnalyzedReviewSentenceCreate(
        sentence="Graphics are not great.",
        prediction="negative",
        gold_label="negative",
        analyzed_review_id=analyzed_review.id,
        created_at=datetime.now()))

    result = await session.execute(select(models.AnalyzedReviewSentence).where(models.AnalyzedReviewSentence.id == sentence1.id))
    sentence1 = result.scalars().first()

    result = await session.execute(select(models.AnalyzedReviewSentence).where(models.AnalyzedReviewSentence.id == sentence2.id))
    sentence2 = result.scalars().first()

    analyzed_review = result.scalars().first()

    assert sentence1.sentence == "This is a test review about great gameplay and such."
    assert sentence1.prediction == "positive"
    assert sentence1.gold_label == "positive"
    assert sentence1.analyzed_review_id == analyzed_review.id
    assert sentence1.created_at is not None

    assert sentence2.sentence == "Graphics are not great."
    assert sentence2.prediction == "negative"
    assert sentence2.gold_label == "negative"
    assert sentence2.analyzed_review_id == analyzed_review.id
    assert sentence2.created_at is not None

    result = await session.execute(select(models.AnalyzedReview)
                                   .where(models.AnalyzedReview.id == analyzed_review.id)
                                   .options(selectinload(models.AnalyzedReview.analyzed_review_sentences)))
    analyzed_review = result.scalars().first()
    assert len(analyzed_review.analyzed_review_sentences) == 2


# test_analyzer.py

@pytest.mark.asyncio
async def test_get_analyzed_reviews_with_search_filter(clear_db, seeded_data, session: AsyncSession):
    # Test retrieving all analyzed reviews
    all_analyzed_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=schemas.AnalyzerSearchFilter())
    assert len(all_analyzed_reviews) == 4

    # Test filtering by task
    filter_task = schemas.AnalyzerSearchFilter(task="task1")
    task_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_task)
    assert len(task_filtered_reviews) == 4

    # Test filtering by model
    filter_model = schemas.AnalyzerSearchFilter(model="model1")
    model_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_model)
    assert len(model_filtered_reviews) == 4

    # Test filtering by prediction
    filter_prediction = schemas.AnalyzerSearchFilter(prediction="positive")
    prediction_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_prediction)
    assert len(prediction_filtered_reviews) == 2

    # Test filtering by gold_label
    filter_gold_label = schemas.AnalyzerSearchFilter(gold_label="positive")
    gold_label_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_gold_label)
    assert len(gold_label_filtered_reviews) == 2

    # Test filtering by review_id
    filter_review_id = schemas.AnalyzerSearchFilter(review_id=1)
    review_id_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_review_id)
    assert len(review_id_filtered_reviews) == 1
    assert review_id_filtered_reviews[0].id == 1

    # Test filtering by analyzed_review_id
    filter_analyzed_review_id = schemas.AnalyzerSearchFilter(analyzed_review_id=1)
    analyzed_review_id_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_analyzed_review_id)
    assert len(analyzed_review_id_filtered_reviews) == 1
    assert analyzed_review_id_filtered_reviews[0].id == 1

    # Test filtering by multiple conditions
    filter_multiple = schemas.AnalyzerSearchFilter(task="task1", model="model1", prediction="positive", gold_label="positive")
    multiple_filtered_reviews = await crud.analyzer.get_analyzed_reviews(session, search_filter=filter_multiple)
    assert len(multiple_filtered_reviews) == 2
