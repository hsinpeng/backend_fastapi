from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

# For API return format
class GenericResponse(BaseModel, Generic[T]):
    message: str
    data: T
