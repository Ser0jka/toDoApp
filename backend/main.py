from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class Task(BaseModel):
    """Модель задачи"""
    id: str
    title: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

# Категории
class Category(BaseModel):
    """Модель Категории"""
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None
    completed: bool | None = None

class CategoryDelete(BaseModel):
    id: str




tasks: list[Task] = []
book = "Самый богатый человек в Вавилоне"
categories: list[Category] = []


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Получить список задач"""
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Создать новую задачу"""
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    """
    Обновить существующую задачу
    task_id получаем из url
    payload получаем из тела запроса
    """
    for task in tasks:
        if task.id == task_id:
            task.title = payload.title if payload.title is not None else task.title
            task.completed = payload.completed if payload.completed is not None else task.completed
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    """Удалить задачу"""
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate):
    """Создать заадачу"""
    category = Category(id=str(uuid4()), name=payload.name)
    categories.append(category)
    return category

@app.get("/categories", response_model=list[Category])
def get_tasks():
    """Получить список задач"""
    return categories

@app.patch("/categories/{cat_id}", response_model=Category)
def update_category(cat_id: str, payload: CategoryUpdate) -> Task:
    for category in categories:
        if category.id == cat_id:
            category.name = payload.name if payload.name is not None else payload.name
            return category
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")

@app.delete("/categories/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(cat_id: str) -> None:
    for category in categories:
        if category.id == cat_id:
            categories.remove(category)
            return
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")


@app.post('/book', response_model=str, status_code=status.HTTP_201_CREATED)
def print_book():
    return f'Любимая книга: {book}'
