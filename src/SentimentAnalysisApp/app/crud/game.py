import logging
from datetime import timedelta, datetime
from typing import List, Optional, Any, Tuple, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import column, update, func, cast, and_, text, or_, case, nullslast, nullsfirst
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from app.crud.base import CRUDBase
from app.db.session import RegConfig
from app.crud.source import crud_source
from app.schemas.game import GameCreate, GameUpdate
from app.schemas.game import CategoryCreate, CategoryUpdate
from app.schemas.game import GameCategoryCreate, GameCategoryUpdate
import logging
from app import models, schemas
from app.core.cursor import encode_cursor, decode_cursor

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)


class CRUDCategory(CRUDBase[models.Category, CategoryCreate, CategoryUpdate]):
    async def get_id_by_name(self, db: AsyncSession, *, name: str) -> Optional[int]:
        logging.debug(f"get_id_by_name: getting category {name} from db")
        result = await db.scalars(select(self.model.id).where(self.model.name == name))
        logging.debug(f"get_by_name: got category {name} from db")
        return result.first()

    async def create_by_name_with_game_multi(self, db: AsyncSession, *, db_game: CategoryUpdate, names: List[str]):
        for name in names:
            db_obj = await self.get_by_name(db, name=name)
            if db_obj is None:
                db_obj = models.Category(name=name)  # type: ignore
            assoc = models.GameCategory(game=db_game)  # type: ignore
            db_obj.games.append(assoc)
            db.add(db_obj)

        await db.commit()

    async def _add_categories_by_name_for_game(self, db: AsyncSession, *, db_game: CategoryUpdate, names: List[str]):
        result = await db.execute(select(self.model.name, self.model.id).where(self.model.name.in_(names)))
        category_ids = result.all()
        category_ids = {name: id for name, id in category_ids}
        db_objs_to_add = []
        for name in names:
            id = category_ids.get(name)
            if id is None:
                db_obj = models.Category(name=name)  # type: ignore
                assoc = models.GameCategory(game=db_game)  # type: ignore
                db_obj.games.append(assoc)
                db_objs_to_add.append(db_obj)
                db_objs_to_add.append(assoc)
            else:
                assoc = models.GameCategory(game=db_game, category_id=id)  # type: ignore
                db_objs_to_add.append(assoc)
        db.add_all(db_objs_to_add)


class CRUDGameCategory(CRUDBase[models.GameCategory, GameCategoryCreate, GameCategoryUpdate]):
    pass


class CRUDGame(CRUDBase[models.Game, GameCreate, GameUpdate]):
    async def get_by_source_id(self, db: AsyncSession, source_id: int, source_game_id: Any) -> Optional[models.Game]:
        result = await db.execute(select(models.GameSource)
                                  .where(and_(models.GameSource.source_id == source_id,
                                              models.GameSource.source_game_id == str(source_game_id)))
                                  .options(selectinload(models.GameSource.game)))
        return result.scalars().first()

    async def get_ids_by_source_game_ids(
            self, db: AsyncSession, source_id: int, source_game_ids: List[str]
    ) -> Dict[str, int]:
        result = await db.execute(select(models.GameSource.source_game_id, models.GameSource.game_id)
                                  .where(and_(models.GameSource.source_id == source_id,
                                              models.GameSource.source_game_id.in_(source_game_ids))))
        return dict(result.all())

    async def get_by_source_game_ids(
            self, db: AsyncSession, source_id: int, source_game_ids: List[str]
    ) -> Dict[str, models.Game]:
        result = await db.scalars(select(models.GameSource)
                                  .where(and_(models.GameSource.source_id == source_id,
                                              models.GameSource.source_game_id.in_(source_game_ids)))
                                  .options(selectinload(models.GameSource.game)))
        return {gs.source_game_id: gs.game for gs in result.all()}

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[models.Category]:
        ts_query = func.plainto_tsquery(cast("english", RegConfig), name)
        stmt = select(self.model).where(
            self.model.name_tsv.bool_op("@@")(ts_query)
        ).limit(5)

        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_source_game_id(self, db: AsyncSession, *, id: int) -> str:
        result = await db.scalars(select(models.GameSource.source_game_id).where(models.GameSource.game_id == id))
        return result.first()

    async def create_from_source(self, db: AsyncSession, *, obj_in: GameCreate, source_id: int,
                                 source_game_id: str) -> models.Game:
        db_obj = self.model(**obj_in.dict())  # type: ignore

        assoc = models.GameSource(
            game=db_obj,  # type: ignore
            source_id=source_id,  # type: ignore
            source_game_id=source_game_id  # type: ignore
        )
        db.add_all([assoc, db_obj])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_categories_by_names(
            self, db: AsyncSession, *, obj_in: GameCreate, names: List[str]
    ) -> models.Game:
        db_obj = self.model(**obj_in.dict(exclude={"source_id", "source_game_id"}))  # type: ignore
        logger.debug(f"creating categories for {obj_in.name}")
        await crud_category._add_categories_by_name_for_game(db, db_game=db_obj, names=names)
        logger.debug(f"created categories for {obj_in.name}")
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_categories_by_names_and_source(
            self, db: AsyncSession, *, obj_in: GameCreate, source_id: int, source_game_id: Any, names: List[str]
    ) -> Optional[models.Game]:
        obj_in_data = obj_in.dict()
        game_db_obj = self.model(**obj_in_data)  # type: ignore
        logger.debug(f"creating categories for {obj_in.name}")
        await crud_category._add_categories_by_name_for_game(db, db_game=game_db_obj, names=names)
        logger.debug(f"created categories for {obj_in.name}")
        game_source_db_obj = models.GameSource(
            game=game_db_obj,  # type: ignore
            source_id=source_id,  # type: ignore
            source_game_id=str(source_game_id)  # type: ignore
        )
        db.add(game_source_db_obj)
        await db.commit()
        await db.refresh(game_db_obj)
        return game_db_obj

    async def get_all_db_games_from_source(self, db: AsyncSession, *, source_id: int) -> List[models.GameSource]:
        result = await db.execute(
            select(models.GameSource)
            .where(
                (models.GameSource.source_id == source_id) &
                (models.GameSource.game_id != None)
            )
        )
        return result.scalars().all()

    async def get_all_not_updated_db_games_from_source(self, db: AsyncSession, *,
                                                       source_id: int,
                                                       check_interval: timedelta = None) -> List[models.GameSource]:
        if check_interval is None:
            check_interval = timedelta(days=1)
        check_time = datetime.now() - check_interval
        result = await db.execute(
            select(models.Game.id, models.GameSource.source_game_id)
            .where(
                (models.Game.id == models.GameSource.game_id) &
                (models.GameSource.source_id == source_id) &
                or_(models.Game.updated_at == None, models.Game.updated_at <= check_time)
            )
        )
        return result.all()

    async def get_ids_and_source_ids_for_reviews_scraping_from_source(
            self, db: AsyncSession, *,
            source_id: int,
            check_interval: timedelta = None
    ) -> List[Tuple[id, str]]:
        """Get all games from source that need to be scraped for reviews determined by check_interval
        or if they have never been scraped before.
        """
        if check_interval is None:
            check_interval = timedelta(days=1)
        check_time = datetime.now() - check_interval
        result = await db.execute(
            select(models.GameSource.game_id, models.GameSource.source_game_id)
            .where(
                (models.GameSource.game_id != None) &
                (models.GameSource.source_id == source_id) &
                or_(models.GameSource.reviews_scraped_at == None, models.GameSource.reviews_scraped_at <= check_time)
            )
        )
        return result.all()

    async def get_all_app_ids_from_source(self, db: AsyncSession, *, source_id: int) -> List[int]:
        result = await db.execute(
            select(models.GameSource.source_game_id).where(models.GameSource.source_id == source_id))
        return result.scalars().all()

    async def create_non_game_app_from_source(self, db: AsyncSession, *,
                                              source_id: int, source_obj_id: Any):
        game_source_db_obj = models.GameSource(
            source_id=source_id,  # type: ignore
            source_game_id=str(source_obj_id)  # type: ignore
        )
        db.add(game_source_db_obj)
        await db.commit()

    async def _create_from_source(self, db: AsyncSession, *,
                                  obj_in: GameCreate,
                                  source_id: int,
                                  source_game_id: Any) -> Optional[models.Game]:
        db_obj = await self.get_by_source_id(db,
                                             source_id=source_id,
                                             source_game_id=source_game_id)
        if db_obj is not None:
            return db_obj

        db_obj = await self.get_by_name(db, name=obj_in.name)
        if db_obj is None:
            # db_obj = await self.create_with_categories_by_names_and_source(db,
            #                                                                obj_in=obj_in,
            #                                                                names=[c.name for c in obj_in.categories])
            db_obj = models.Game(**obj_in.dict(exclude={"source_id", "source_game_id", "categories"}))  # type: ignore
            db.add(db_obj)

        game_source_db_obj = models.GameSource(source_id=source_id,  # type: ignore
                                               source_game_id=str(source_game_id))  # type: ignore
        game_source_db_obj.game = db_obj
        db.add(game_source_db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_num_reviews(self, db: AsyncSession, *, id: int):
        # update column num_reviews of table models.Game with id=id by summing up all rows of table models.Review where game_id=id
        await db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(num_reviews=select(func.count(models.Review.id)).where(models.Review.game_id == id))
        )
        await db.commit()

    async def update_after_reviews_scrape(
            self, db: AsyncSession, *,
            source_id: int,
            game_id: Optional[int] = None,
            source_game_id: Optional[str] = None
    ):
        if game_id is None and source_game_id is None:
            raise ValueError("game_id or source_game_id must be provided")
        if game_id is not None:
            db_obj = await db.scalar(
                select(models.GameSource)
                .where((models.GameSource.game_id == game_id) & (models.GameSource.source_id == source_id)))
        else:
            db_obj = await db.scalar(
                select(models.GameSource)
                .where(
                    (models.GameSource.source_game_id == source_game_id) & (models.GameSource.source_id == source_id)))
        if db_obj is None:
            return
        num_reviews = await db.scalar(select(func.count(models.Review.id))
        .where(
            (models.Review.game_id == db_obj.game_id) & (models.Review.source_id == source_id)))
        db_obj.reviews_scraped_at = datetime.now()
        db_obj.num_reviews = num_reviews
        await db.commit()

    async def add_category(self, db: AsyncSession, *, game_id: int, category_id: int):
        db_obj = models.GameCategory(game_id=game_id, category_id=category_id)
        db.add(db_obj)
        await db.commit()

    async def add_developer(self, db: AsyncSession, *, game_id: int, developer_id: int):
        db_obj = models.GameDeveloper(game_id=game_id, developer_id=developer_id)
        db.add(db_obj)
        await db.commit()

    async def add_categories(self, db: AsyncSession, *, game_id: int, categories: List[int]):
        for category in categories:
            db_obj = models.GameCategory(game_id=game_id, category_id=category)
            db.add(db_obj)
        await db.commit()

    async def add_developers(self, db: AsyncSession, *, game_id: int, developers: List[int]):
        for developer in developers:
            db_obj = models.GameDeveloper(game_id=game_id, developer_id=developer)
            db.add(db_obj)
        await db.commit()

    async def get_sources(self, db: AsyncSession, *, game_id: int) -> List[models.Source]:
        result = await db.execute(select(models.GameSource)
                                  .where(models.GameSource.game_id == game_id)
                                  .options(selectinload(models.GameSource.source)))
        gs = result.scalars().all()
        return [g.source for g in gs]

    async def get_game_list(self, db: AsyncSession, *,
                            limit: int = 100,
                            offset: int = 0,
                            sort: schemas.GameListSort = None,
                            filter: schemas.GameListFilter = None
                            ) -> schemas.GameListResponse:
        game_score = (
            func.coalesce(
                (func.sum(
                    case(
                        (models.Aspect.polarity == "positive", 2.0),
                        (models.Aspect.polarity == "negative", -2.0),
                        (models.Aspect.polarity == "neutral", 0.5),
                        else_=0.0)
                ) / (func.count(models.Aspect.id.distinct()) + 1.0)) + 5.0,
                5.0)).label("score")

        stmt = select(self.model, game_score, func.count(models.Review.id.distinct())).select_from(self.model) \
            .outerjoin(models.Review) \
            .outerjoin(models.Aspect) \
            .group_by(self.model.id) \
            .options(selectinload(self.model.categories).selectinload(models.GameCategory.category),
                     selectinload(self.model.developers).selectinload(models.GameDeveloper.developer))

        filters = []
        if filter:
            if filter.name is not None:
                ts_query = func.plainto_tsquery(cast("english", RegConfig), filter.name)
                filters.append(self.model.name_tsv.bool_op("@@")(ts_query))

            if filter.categories is not None:
                filters.append(self.model.categories.any(models.GameCategory.name.in_(filter.categories)))

            if filter.developers is not None:
                filters.append(self.model.developers.any(models.GameDeveloper.name.in_(filter.developers)))

            if filter.min_release_date is not None:
                filters.append(self.model.release_date >= filter.min_release_date)

            if filter.max_release_date is not None:
                filters.append(self.model.release_date <= filter.max_release_date)

            if filter and filter.min_score is not None or filter.max_score is not None:
                score_subquery = select(self.model.id.label("id")).select_from(self.model) \
                    .outerjoin(models.Review) \
                    .outerjoin(models.Aspect) \
                    .group_by(self.model.id) \
                    .having(
                    and_(
                        game_score >= (filter.min_score if filter.min_score is not None else -float('inf')),
                        game_score <= (filter.max_score if filter.max_score is not None else float('inf'))
                    )
                )
                filters.append(self.model.id.in_(score_subquery))
            if filter and filter.min_num_reviews is not None or filter.max_num_reviews is not None:
                review_subquery = select(self.model.id).select_from(self.model) \
                    .outerjoin(models.Review) \
                    .group_by(self.model.id) \
                    .having(
                    and_(
                        func.count(models.Review.id.distinct()) >= (
                            filter.min_num_reviews if filter.min_num_reviews is not None else -float('inf')),
                        func.count(models.Review.id.distinct()) <= (
                            filter.max_num_reviews if filter.max_num_reviews is not None else float('inf'))
                    )
                )
                filters.append(self.model.id.in_(review_subquery))

        if sort:
            if sort.num_reviews is not None:
                if sort.num_reviews == "asc":
                    stmt = stmt.order_by(func.count(models.Review.id.distinct()).asc())
                else:
                    stmt = stmt.order_by(func.count(models.Review.id.distinct()).desc())
            elif sort.score is not None:
                if sort.score == "asc":
                    stmt = stmt.order_by(nullslast(game_score.asc()))
                else:
                    stmt = stmt.order_by(nullslast(game_score.desc()))
            elif sort.release_date is not None:
                if sort.release_date == "asc":
                    stmt = stmt.order_by(nullslast(self.model.release_date.asc()))
                else:
                    stmt = stmt.order_by(nullslast(self.model.release_date.desc()))
            elif sort.name is not None:
                if sort.name == "asc":
                    stmt = stmt.order_by(nullslast(self.model.name.asc()))
                else:
                    stmt = stmt.order_by(nullslast(self.model.name.desc()))

        count_stmt = select(func.count(self.model.id.distinct())).select_from(self.model).outerjoin(
            models.Review).outerjoin(
            models.Aspect).filter(and_(True, *filters))
        count_result = await db.execute(count_stmt)
        total_count = count_result.scalar()
        summary = schemas.GameListQuerySummary(total=total_count)

        stmt = stmt.filter(and_(True, *filters)).order_by(self.model.id).limit(limit).offset(offset)
        result = await db.execute(stmt)
        games = result.all()
        games = [schemas.GameListItem(
            id=g.id,
            name=g.name,
            image_url=g.image_url,
            release_date=g.release_date,
            categories=[schemas.Category.from_orm(c.category) for c in g.categories],
            developers=[schemas.Developer.from_orm(d.developer) for d in g.developers],
            score=round(score, 1),
            num_reviews=num_reviews
        ) for g, score, num_reviews in games]

        return schemas.GameListResponse(
            games=games,
            query_summary=summary
        )

    async def get_matches(self, db: AsyncSession, *, name: str, limit: int = 10) -> List[models.Game]:
        ts_query = func.plainto_tsquery(cast("english", RegConfig), name)
        stmt = select(self.model.name).where(
            self.model.name_tsv.bool_op("@@")(ts_query)
        ).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()


crud_game = CRUDGame(models.Game)
crud_category = CRUDCategory(models.Category)
crud_game_category = CRUDGameCategory(models.GameCategory)
