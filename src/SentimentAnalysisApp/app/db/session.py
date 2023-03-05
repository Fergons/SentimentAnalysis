from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.type_api import UserDefinedType

from app.core import config

if config.settings.ENVIRONMENT == "PYTEST":
    sqlalchemy_database_uri = config.settings.TEST_SQLALCHEMY_DATABASE_URI
elif config.settings.ENVIRONMENT == "PRODUCTION":
    sqlalchemy_database_uri = config.settings.PRODUCTION_SQLALCHEMY_DATABASE_URI
else:
    sqlalchemy_database_uri = config.settings.DEFAULT_SQLALCHEMY_DATABASE_URI

async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


class RegConfig(UserDefinedType):
    """regconfig type for FTS.

    https://www.postgresql.org/docs/current/datatype-oid.html
    #DATATYPE-OID-TABLE
    """
    cache_ok = True
    def get_col_spec(self, **kwargs: Any) -> str:
        return 'regconfig'