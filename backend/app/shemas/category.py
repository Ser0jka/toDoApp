from pydantic import BaseModel, ConfigDict



class CategoryShema(BaseModel):
    """Модель задачи"""
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str

class CategoryCreateShema(BaseModel):
    name: str

class CategoryUpdateShema(BaseModel):
    name: str | None = None