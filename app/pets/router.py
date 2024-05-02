from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette import status

from app.auth.dependencies import get_current_user
from app.exceptions import IncorrectIDException
from app.pets.dao import PetDAO
from app.pets.schemas import SPetAdd, SPetGet
from app.users.models import User

router = APIRouter(prefix="/pets", tags=["Pets"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_pet(pet: SPetAdd, user: User = Depends(get_current_user)):
    pet_data = pet.model_dump()
    pet_data["user_id"] = user.id
    await PetDAO.add(**pet_data)


@router.get("/get", status_code=status.HTTP_200_OK)
@cache(expire=2)
async def get_pet(user: User = Depends(get_current_user)) -> list[dict[str, SPetGet]]:
    pets = await PetDAO.fetch_all(user_id=user.id)
    return pets


@router.delete("/del", status_code=status.HTTP_200_OK)
async def remove_pet(pet_id: int, user: User = Depends(get_current_user)):
    result = await PetDAO.delete(id=pet_id, user_id=user.id)
    if not result:
        raise IncorrectIDException
