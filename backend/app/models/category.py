from sqlalchemy.orm import Mapped

from models.base import Base


class CategoryORM(Base):
    """Модель для таблицы категорий в Базе Данных"""

    __tablename__ = "categories"

    name: Mapped[str]
