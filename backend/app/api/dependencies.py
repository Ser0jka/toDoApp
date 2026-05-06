from fastapi import Depends
from app.services.task import TaskService
from app.services.category import CategoryService
from app.db import session
from app.db.session import get_db



def get_task_service(db: session = Depends(get_db)) -> TaskService:
    return TaskService(db)

def get_category_service(db: session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)