from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_task_service
from app.services.task import TaskNotFound, TaskService
from app.shemas.task import TaskCreateShema, TaskShema, TaskUpdateShema

router = APIRouter(prefix="/tasks")


@router.get("")
def get_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskShema]:
    return task_service.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateShema, task_service: TaskService = Depends(get_task_service)
) -> TaskShema:
    return task_service.create_task(task_create=payload)


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateShema,
    task_service: TaskService = Depends(get_task_service),
) -> TaskShema:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str, task_service: TaskService = Depends(get_task_service)
) -> None:
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
