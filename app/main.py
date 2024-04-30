from fastapi import FastAPI, Query
from sqladmin import Admin

from app.admin.views import UserAdmin, AppointmentAdmin
from app.auth.router import router as auth_router
from app.database import engine
from app.users.router import router as user_router
from app.pets.router import router as pet_router
from app.services.router import router as service_router
from app.appointment.router import router as appointment_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(pet_router)
app.include_router(service_router)
app.include_router(appointment_router)


admin = Admin(app, engine)


admin.add_view(UserAdmin)
admin.add_view(AppointmentAdmin)
