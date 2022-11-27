from .user import User, UserCreate, UserDB, UserUpdate
from .game import Game, GameBase, GameCreate, GameUpdate, GameInDB, GameInDBBase
from .game import Category, CategoryBase, CategoryUpdate, CategoryCreate
from .review import Review, ReviewBase, ReviewCreate, ReviewUpdate, ReviewInDB, ReviewInDBBase
from .reviewer import Reviewer, ReviewerBase, ReviewerCreate, ReviewerUpdate, ReviewerInDB, ReviewerInDBBase
from .aspect import Aspect, AspectBase, AspectCreate, AspectUpdate, AspectInDB, AspectInDBBase
from .source import Source, SourceBase, SourceCreate, SourceUpdate, SourceInDBBase
from .game import GameFromSourceCreate

Reviewer.update_forward_refs(Review=Review, Source=Source)
Game.update_forward_refs(Review=Review, Source=Source)
Category.update_forward_refs(Review=Review, Source=Source)
Review.update_forward_refs(Game=Game, Source=Source, Aspect=Aspect, Reviewer=Reviewer)
Aspect.update_forward_refs(Review=Review,)
Source.update_forward_refs(Game=Game, Review=Review, Reviewer=Reviewer)
GameFromSourceCreate.update_forward_refs(Source=Source)
ReviewCreate.update_forward_refs(ReviewerCreate=ReviewerCreate)
