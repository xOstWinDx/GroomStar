from pydantic import BaseModel, ConfigDict


class SServicesAdd(BaseModel):
    title: str | None = None
    description: str | None = None
    price_small: int | None = None
    price_big: int | None = None


class SServicesGet(SServicesAdd):
    id: int
