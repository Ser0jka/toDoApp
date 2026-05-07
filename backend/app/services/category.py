from unicodedata import category
from sqlalchemy.orm import Session
from app.repositories.category import CategoryRepository
from app.shemas.category import CategoryShema, CategoryCreateShema, CategoryUpdateShema

class CategoryNotFound(Exception):
    """Задача не найдена"""



class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategoryShema]:
       categories = self.category_repository.get_all()

       return [CategoryShema.model_validate(category) for category in categories]
    
    def create_category(self, cat_create: CategoryCreateShema) -> CategoryShema:
        category = self.category_repository.create(title=cat_create.name)
        self.db.commit()
        return CategoryShema.model_validate(category)
 

    def update_category(self, category_id: str, category_update: CategoryUpdateShema) -> CategoryShema:
        category = self.category_repository.get_by_id(cat_id=category_id)
        if not category:
            raise CategoryNotFound("Категория не найдена")
        if category_update.name:
            category.name = category_update.name
        self.db.commit()
        return CategoryShema.model_validate(category)


    def delete_category(self, category_id: str) -> None:
        category = self.category_repository.get_by_id(cat_id=category_id)
        if not category:
            raise CategoryNotFound("Категория не найдена")
        self.category_repository.delete(category)
        self.db.commit()
        return None