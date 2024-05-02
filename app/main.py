from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

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
from app.pages.router import router as page_router
from app.images.router import router as image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


sentry_sdk.init(
    dsn=settings.SENTRY,
    enable_tracing=True,
)


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(pet_router)
app.include_router(service_router)
app.include_router(appointment_router)
app.include_router(employee_router)
app.include_router(page_router)
app.include_router(image_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(AppointmentAdmin)
admin.add_view(PetAdmin)
admin.add_view(EmployeeAdmin)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
