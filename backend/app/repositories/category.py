from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, cat_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, cat_id)

    def create(self, title: str) -> CategoryORM:
        category = CategoryORM(name=title)
        self.db.add(category)
        return category

    def delete(self, CategoryORM) -> None:
        self.db.delete(CategoryORM)
