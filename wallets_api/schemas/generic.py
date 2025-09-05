
from pydantic import BaseModel


class GenericResponse(BaseModel):
    status: str
    detail: str
