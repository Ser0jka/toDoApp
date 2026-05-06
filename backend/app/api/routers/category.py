from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.dependencies import get_category_service

from app.services.category import CategoryNotFound, CategoryService
from app.shemas.category import CategoryCreateShema, CategoryShema, CategoryUpdateShema

router = APIRouter(prefix="/categories")

@router.get("")
def get_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategoryShema]:
    return category_service.list_categories()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateShema, category_service: CategoryService = Depends(get_category_service)) -> CategoryShema:
    return category_service.create_category(cat_create=payload)

@router.patch("/{category_id}")
def update_category(category_id: str, payload: CategoryCreateShema, category_service: CategoryService = Depends(get_category_service)) -> CategoryShema:
    try:
        return category_service.update_category(cat_id=category_id, category_update=payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")



@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service: CategoryService = Depends(get_category_service)) -> None:
    try:
        return category_service.delete_category(task_id=category_id)
    except CategoryNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")