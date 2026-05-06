from pydantic import BaseModel, ConfigDict



class CategoryShema(BaseModel):
    """Модель задачи"""
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str

class CategoryCreateShema(BaseModel):
    title: str

class CategoryUpdateShema(BaseModel):
    title: str | None = None