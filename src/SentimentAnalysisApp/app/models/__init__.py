"""
Created by Frantisek Sabol
Alembic uses this file to check if database schema changed
"""
from app.db.base_class import Base
from .review import Review
from .game import Game, Category, GameCategory, GameDeveloper
from .reviewer import Reviewer
from .source import Source, GameSource
from .aspect import Aspect
from .user import User
from .developer import Developer
from .analyzer import AnalyzedReview, AnalyzedReviewSentence
