from fastapi import APIRouter, Depends, HTTPException, Body

from app.auth.dependencies import get_current_user_admin
from app.services.dao import ServicesDAO
from app.services.schemas import SServicesAdd, SServicesGet

router = APIRouter(tags=["Services"], prefix="/services")


@router.post("/add")
async def add_services(
    service_data: SServicesAdd, user=Depends(get_current_user_admin)
):
    await ServicesDAO.add(**service_data.model_dump())


@router.delete("/del")
async def del_services(service_id: int, user=Depends(get_current_user_admin)):
    res = await ServicesDAO.delete(id=service_id)
    if not res:
        raise HTTPException(status_code=400, detail="Неверные данные")


@router.get("/get")
async def get_services(
    user=Depends(get_current_user_admin),
) -> list[dict[str, SServicesGet]]:
    return await ServicesDAO.fetch_all()


@router.patch("/update")
async def update_services(
    service_id: int,
    new_values: SServicesAdd,
    user=Depends(get_current_user_admin),
):
    res = await ServicesDAO.update(
        service_id, **new_values.model_dump(exclude_none=True)
    )
    if not res:
        raise HTTPException(status_code=400, detail="Неверные данные")
