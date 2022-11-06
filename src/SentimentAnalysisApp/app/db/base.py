# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User # noqa
from app.models.game import Game  # noqa
from app.models.aspect import Aspect  # noqa
from app.models.review import Review  # noqa
from app.models.reviewer import Reviewer  # noqa