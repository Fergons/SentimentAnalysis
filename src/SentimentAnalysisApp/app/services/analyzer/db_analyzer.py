import asyncio
import json
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from .utils import clean
from app import crud, schemas, models
from app.db.session import async_session
import tqdm
import findfile
from .acos import data_utils
import argparse
import pathlib
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)


async def dump_all_analyzed_reviews_to_file(db: AsyncSession):
    reviews = await crud.review.get_with_aspects(db)
    with open("./reviews/review_id_text_aspects.txt", "w", encoding="utf-8") as f:
        for review in reviews:
            aspect_list = [
                {
                    "term": aspect.term,
                    "polarity": aspect.polarity,
                    "category": aspect.category,
                    "opinion": aspect.opinion
                } for aspect in review.aspects
            ]
            aspect_string = json.dumps(aspect_list, ensure_ascii=False)
            f.write(f"{review.id}\t{review.text}\t{aspect_string}")


async def analyze_db_reviews(db: AsyncSession, game_id: int = None, task="joint-acos", model_name="mt5-acos-1.0", **kwargs):
    batch_size = kwargs.get("batch_size", 100)
    if task == "joint-acos":
        from .acos import model as acos_model
        if model_name is None:
            model_dir = findfile.find_dir(f"{pathlib.Path(__file__).parent.resolve()}/acos/models", key=["mt5"])
            model_name = model_dir.rsplit("/",1)[-1]
        else:
            model_dir = findfile.find_dir(f"{pathlib.Path(__file__).parent.resolve()}/acos/models", key=[model_name])
        if not model_dir:
            raise ValueError(f"Model {model_name} not found")
        model = acos_model.ABSAGenerator(model_dir)
    else:
        raise ValueError(f"Task {task} not supported")

    num_reviews_to_process = await crud.review.count_not_processed_reviews(db, game_id=game_id)
    logger.info(f"Found {num_reviews_to_process} reviews to process")
    last_id = None
    for _ in tqdm.tqdm(range(num_reviews_to_process // batch_size + 1), desc="Analyzing reviews"):
        reviews = await crud.review.get_not_processed_by_game(db, limit=batch_size, game_id=game_id, last_id=last_id)
        last_id = reviews[-1].id
        cleaned_texts = [clean(review.text) for review in reviews]
        results = model.batch_predict(batch=cleaned_texts, task=task, max_length=128)
        for review, result in zip(reviews, results):
            prediction = data_utils.create_task_output_string(task, outputs=result["Quadruples"])
            analyzed_review_in = schemas.AnalyzedReviewCreate(
                cleaned_text=result["text"],
                review_id=review.id,
                model=model_name,
                task=task,
                prediction=prediction,
                created_at=datetime.now()
            )
            await crud.analyzed_review.create(db, obj_in=analyzed_review_in)
            aspects_to_create = []
            for aspect in result["Quadruples"]:
                if aspect["category"] == "NULL" or aspect["polarity"] == "NULL":
                    continue
                aspect_in = schemas.AspectCreate(
                    review_id=review.id,
                    term=aspect["aspect"],
                    category=aspect["category"],
                    polarity=aspect["polarity"],
                    opinion=aspect["opinion"],
                    model_id=model_name)
                aspects_to_create.append(aspect_in)
            await crud.aspect.create_multi(db, objs_in=aspects_to_create)
            await crud.review.update(db, db_obj=review, obj_in=schemas.ReviewUpdate(processed_at=datetime.now()))

async def main(args):
    async with async_session() as db:
        if args.analyze:
            await analyze_db_reviews(db, game_id=args.game_id, task=args.task, model_name=args.model)
        if args.dump:
            await dump_all_analyzed_reviews_to_file(db)
        print("Done...")


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--dump", action="store_true")
    argparse.add_argument("--analyze", action="store_true")
    argparse.add_argument("--game_id", type=int, default=None, required=True)
    argparse.add_argument("--task", type=str, default="joint-acos")
    argparse.add_argument("--model", type=str, default="mt5-acos-1.0")
    args = argparse.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))

