from fastapi import FastAPI, Query
from securecookies import SecureCookiesMiddleware
from sqladmin import Admin
from starlette.middleware import Middleware

from app.admin.auth import AdminAuth
from app.admin.views import UserAdmin, AppointmentAdmin, PetAdmin, EmployeeAdmin
from app.auth.router import router as auth_router
from app.config import settings
from app.database import engine
from app.users.router import router as user_router
from app.pets.router import router as pet_router
from app.services.router import router as service_router
from app.appointment.router import router as appointment_router
from app.employee.router import router as employee_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(pet_router)
app.include_router(service_router)
app.include_router(appointment_router)
app.include_router(employee_router)

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(AppointmentAdmin)
admin.add_view(PetAdmin)
admin.add_view(EmployeeAdmin)
