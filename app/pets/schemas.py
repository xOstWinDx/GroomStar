from typing import Literal, Annotated

from pydantic import BaseModel, Field


class SPetAdd(BaseModel):
    name: str
    species: Literal["Собака", "Кошка", "Другое"]
    breed: str


class SPetGet(SPetAdd):
    user_id: int
    id: int
