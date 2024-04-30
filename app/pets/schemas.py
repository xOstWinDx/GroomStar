from pydantic import BaseModel, Field


class SPetAdd(BaseModel):

    name: str
    species: str
    breed: str


class SPetGet(SPetAdd):
    user_id: int
    id: int
