"""
SQL Alchemy models declaration.

Note, imported by alembic migrations logic, see `alembic/env.py`
"""
from app.db.base_class import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class User(Base, SQLAlchemyBaseUserTable):
    pass

