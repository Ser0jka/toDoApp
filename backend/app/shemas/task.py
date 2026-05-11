from pydantic import BaseModel, ConfigDict


class TaskShema(BaseModel):
    """Модель задачи"""

    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    completed: bool = False


class TaskCreateShema(BaseModel):
    title: str


class TaskUpdateShema(BaseModel):
    title: str | None = None
    completed: bool | None = None
