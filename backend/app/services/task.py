from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.shemas.task import TaskShema, TaskCreateShema, TaskUpdateShema

class TaskNotFound(Exception):
    """Задача не найдена"""



class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskShema]:
       tasks = self.task_repository.get_all()

       return [TaskShema.model_validate(task) for task in tasks]
    
    def create_task(self, task_create: TaskCreateShema) -> TaskShema:
        task =self.task_repository.create(title=task_create.title)
        self.db.commit()
        return TaskShema.model_validate(task)
 

    def update_task(self, task_id: str, task_update: TaskUpdateShema) -> TaskShema:
        task = self.task_repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskNotFound("Задача не найдена")
        if task_update.title:
            task.title = task_update.title
        if task_update.completed is not None:
            task.completed = task_update.completed
        self.db.commit()
        return TaskShema.model_validate(task)


    def delete_task(self, task_id: str) -> None:
        task = self.task_repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskNotFound("Задача не найдена")
        self.task_repository.delete(task)
        self.db.commit()
        return None