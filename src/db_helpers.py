import psycopg
import asyncio
import logging

from data.private.keys import POSTGRES_USER,POSTGRES_PASSWORD


class DatabaseHandler:
    def __init__(self, dbname="reviewanalysis", **kwargs):
        self.dbname = dbname
        self.user = kwargs.get("user", POSTGRES_USER)
        self.password = kwargs.get("password", POSTGRES_PASSWORD)
        self.host = kwargs.get("host", "127.0.0.1")
        self.default_connect_string = f"dbname={self.dbname} "\
                                     f"user={self.user} "\
                                     f"password={self.password} "\
                                     f"host={self.host}"


    async def update(self, *args):
        """
        updates all games that are due to update
        or updates games with respective game_ids that
        were passed to this function as positional arguments
        """
        if not args:
            await self.update_all()
        else:
            await self._update(*args)

    async def _update(self, *args):
        results = await asyncio.gather(*map(self.update_game, args))

    async def update_all(self):
        async with await psycopg.AsyncConnection.connect(
                self.default_connect_string,
                autocommit=True
        ) as conn:
            async with conn.cursor() as cursor:
                cursor.execute()

    async def update_game(self, **kwargs):
        keys = kwargs.keys()
        values = kwargs.values()
        async with await psycopg.AsyncConnection.connect(
                self.default_connect_string,
                autocommit=True
        ) as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(f"""INSERT INTO games ({",".join(keys)})
                                      VALUES({",".join([f"%({i})s" for i in keys])}) 
                                      ON CONFLICT (game_id) DO 
                                      UPDATE SET {", ".join([f"{k}=%({k})s" for k in keys])}""", kwargs)
                except psycopg.errors.UniqueViolation:
                    return False
                else:
                    return cursor.rowcount == 1


    async def add_game(self, **kwargs):
        pass


    async def add_steam_game_by_name(self, name):
        pass

    async def setup(self):
        await self.db_setup()

    async def db_setup(self, **kwargs):
        """
        tries to connect to a database named dbname,
         if the database is not found, attempts to create a new database named dbname
        """
        dbname = self.dbname.lower()
        try:
            logger.log(logging.INFO, f"Trying to connect to database '{self.dbname}'.")
            conn = await psycopg.AsyncConnection.connect(
                self.default_connect_string,
                autocommit=True,
                **kwargs
            )

        except psycopg.OperationalError:
            logger.log(logging.INFO, f"Database named '{dbname}' not found.")
            async with await psycopg.AsyncConnection.connect(
                self.default_connect_string,
                autocommit=True,
                dbname="postgres"
            ) as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"CREATE database {dbname}")

            async with await psycopg.AsyncConnection.connect(
                    self.default_connect_string,
                    autocommit=True,
                    **kwargs
            ) as conn:
                async with conn.cursor() as cursor:
                    await create_games_table(cursor)
                    await create_reviews_table(cursor)

            logger.log(logging.INFO, f"Database '{dbname}' created!")

        else:
            logger.log(logging.INFO, f"Database named '{dbname}' already exists.")
            async with conn.cursor() as cursor:
                await cursor.execute("""
                SELECT EXISTS(SELECT 1 FROM information_schema.tables 
                    WHERE table_catalog=%s AND table_name='games');
                """, (dbname,))
                rv = await cursor.fetchone()
                if not any(rv):
                    await create_games_table(cursor)

                await cursor.execute("""
                SELECT EXISTS(SELECT 1 FROM information_schema.tables 
                    WHERE table_catalog=%s AND table_name='reviews');
                """, (dbname,))
                rv = await cursor.fetchone()
                if not any(rv):
                    await create_reviews_table(cursor)

            await conn.close()


async def create_games_table(cursor):
    await cursor.execute("""
    
        DROP TABLE IF EXISTS games;
        CREATE UNLOGGED TABLE games (
            game_id                             INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            name                                TEXT,
            steam_app_id                        INTEGER UNIQUE,
            metacritic_user_reviews_url         TEXT,
            gamespot_review_url                 TEXT,
            gamespot_user_reviews_url           TEXT,
            image_url                           TEXT,                        
            metacritic_updated_at               TIMESTAMP with time zone,
            steam_updated_at                    TIMESTAMP with time zone,  
            gamespot_updated_at                 TIMESTAMP with time zone,
            info_updated_at                     TIMESTAMP with time zone,
            release_timestamp                   TIMESTAMP with time zone
            
        );
        
        """)
    logger.log(logging.INFO, f"Table 'games' created.")


async def create_reviews_table(cursor):
    await cursor.execute("""
    
        DROP TABLE IF EXISTS reviews;
        CREATE UNLOGGED TABLE reviews (
            id                  INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            game_id             INTEGER REFERENCES games(game_id) NOT NULLABLE,
            language            TEXT,
            review              TEXT,
            summary             TEXT,
            score               REAL,
            helpful_score       REAL,
            weighted_score      REAL,
            good                TEXT,
            bad                 TEXT,
            created_at          TIMESTAMP with time zone
            
        );
    """)
    logger.log(logging.INFO, f"Table 'reviews' created.")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    db = DatabaseHandler()
    asyncio.get_event_loop().run_until_complete(db.setup())

