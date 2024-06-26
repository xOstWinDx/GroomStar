from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.auth.dependencies import get_current_user_admin
from app.employee.dao import EmployeeDAO
from app.employee.schemas import SEmployeeAdd, SEmployeeGet
from app.exceptions import IncorrectIDException

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/get", status_code=200)
async def get_employee(
    user=Depends(get_current_user_admin),
) -> list[dict[str, SEmployeeGet]]:
    return await EmployeeDAO.fetch_all()


@router.post("/add", status_code=201)
async def add_employee(
    employee_data: SEmployeeAdd, user=Depends(get_current_user_admin)
):
    try:
        await EmployeeDAO.add(**employee_data.model_dump())
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete("/remove", status_code=200)
async def remove_employee(employee_id: int, user=Depends(get_current_user_admin)):
    if await EmployeeDAO.delete(id=employee_id) == 0:
        raise IncorrectIDException
