import re
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import CategoryORM

class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()
    
    def get_by_id(self, cat_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, cat_id)
    
    def create(self, title: str) -> CategoryORM:
        category = CategoryORM(title=title)
        self.db.add(category)
        return category

    def delete(self, CategoryORM) -> None:
        self.db.delete(CategoryORM)
