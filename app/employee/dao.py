from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import get_async_session
from app.employee.models import Employee


class EmployeeDAO(BaseDAO):
    model = Employee
