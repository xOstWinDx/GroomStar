from app.dao.base import BaseDAO
from app.pets.models import Pet


class PetDAO(BaseDAO):
    model = Pet
