import asyncio
import json
from datetime import datetime
from typing import List
import pickle
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
from nltk import sent_tokenize

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


async def analyze_db_reviews(db: AsyncSession, game_id: int = None, task="joint-acos",
                             model_name="mt5-acos-1.0", **kwargs):
    batch_size = kwargs.get("batch_size", 100)
    dump = kwargs.get("dump", False)
    dump_dir = None
    if dump:
        dump_dir = pathlib.Path("dump")
        dump_dir.mkdir(parents=True, exist_ok=True)

    if task == "joint-acos":
        from .acos import model as acos_model
        if model_name is None:
            model_dir = findfile.find_dir(f"{pathlib.Path(__file__).parent.resolve()}/acos/models", key=["mt5"])
            model_name = model_dir.rsplit("/", 1)[-1]
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
        # check if long reviews are present and join with respective review id zipped
        short_reviews = []
        short_cleaned_texts = []
        long_reviews_output = {}

        for review, text in zip(reviews, cleaned_texts):
            if len(text) > 200:
                long_reviews_output[review.id] = schemas.AnalyzedReviewCreate(
                    cleaned_text=text,
                    review_id=review.id,
                    model=model_name,
                    task=task,
                    prediction="",
                    created_at=datetime.now()
                )
                sentences = sent_tokenize(text, language=review.language)
                for sentence in sentences:
                    short_reviews.append(review)
                    short_cleaned_texts.append(sentence)
            else:
                short_reviews.append(review)
                short_cleaned_texts.append(text)

        try:
            results = model.batch_predict(batch=short_cleaned_texts, task=task, max_length=128)
        except Exception as e:
            logger.error(f"Error while processing batch: {e}")
            continue

        analyzed_reviews_in = []
        aspects_in = []
        for review, result in zip(short_reviews, results):
            for aspect in result["Quadruples"]:
                if aspect["category"] not in ("gameplay", "overall", "other", "audio_visuals", "performance_bugs",
                                              "community") \
                        or aspect["polarity"] not in ("positive", "negative", "neutral"):
                    continue
                aspect_in = schemas.AspectCreate(
                    review_id=review.id,
                    term=aspect["aspect"],
                    category=aspect["category"],
                    polarity=aspect["polarity"],
                    opinion=aspect["opinion"],
                    model_id=model_name)
                aspects_in.append(aspect_in)

            prediction = data_utils.create_task_output_string(task, outputs=result["Quadruples"])
            if review.id in long_reviews_output:
                long_reviews_output[review.id].prediction = "|".join([long_reviews_output[review.id].prediction, prediction])
                continue

            analyzed_review_in = schemas.AnalyzedReviewCreate(
                cleaned_text=result["text"],
                review_id=review.id,
                model=model_name,
                task=task,
                prediction=prediction,
                created_at=datetime.now()
            )
            analyzed_reviews_in.append(analyzed_review_in)

        for analyzed_review_in in long_reviews_output.values():
            analyzed_reviews_in.append(analyzed_review_in)

        await crud.review.update_multi(
            db, db_objs=reviews, objs_in=[schemas.ReviewUpdate(processed_at=datetime.now())] * len(reviews))
        if not dump:
            await crud.aspect.create_multi(db, objs_in=aspects_in)
            await crud.analyzed_review.create_multi(db, objs_in=analyzed_reviews_in)
        else:
            file = dump_dir / f"dumped_analysis_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')}.insert.pkl"
            with file.open("wb") as f:
                map = {
                    "analyzed_reviews": analyzed_reviews_in,
                    "aspects": aspects_in
                }
                pickle.dump(map, f)


async def insert_from_dumped_file(sessionmaker: AsyncSession, file: pathlib.Path = None):
    dump_dir = pathlib.Path("dump")
    files = list(dump_dir.glob("*.insert.pkl"))

    for file in tqdm.tqdm(files, desc="Inserting dumped analysis results"):
        tasks = []
        with file.open("rb") as f:
            map = pickle.load(f)
        async with sessionmaker() as db:
            tasks.append(crud.aspect.create_multi(db, objs_in=map["aspects"]))
        async with sessionmaker() as db:
            tasks.append(crud.analyzed_review.create_multi(db, objs_in=map["analyzed_reviews"]))
        await asyncio.gather(*tasks)
        file.unlink()


async def main(args):
    if args.analyze:
        async with async_session() as db:
            if args.all:
                games = await crud.analyzer.get_games_with_unprocessed_reviews(db, limit=100)
                for game in games:
                    await analyze_db_reviews(db, game_id=game.id, task=args.task, model_name=args.model, batch_size=args.batch_size,
                                             dump=args.dump)
            else:
                await analyze_db_reviews(
                    db, game_id=args.game_id, task=args.task, model_name=args.model, batch_size=args.batch_size,
                    dump=args.dump)
    elif args.insert:
        await insert_from_dumped_file(sessionmaker=async_session)
    print("Done...")


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--dump", action="store_true", help="Dump results to file instead of db which is faster")
    argparse.add_argument("--insert", action="store_true", help="Insert dumped results from files")
    argparse.add_argument("--analyze", action="store_true",
                          help="Analyze reviews in db for a game by default (--game_id 'id' or --all)")
    argparse.add_argument("--game_id", type=int, default=None)
    argparse.add_argument("--task", type=str, default="joint-acos")
    argparse.add_argument("--model", type=str, default="mt5-acos-1.0")
    argparse.add_argument("--batch_size", type=int, default=32)
    argparse.add_argument("--all", action="store_true", help="Analyze all games that have unprocessed reviews")
    args = argparse.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
