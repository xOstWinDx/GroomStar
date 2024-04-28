from fastapi import FastAPI, Query

from app.auth.router import router as auth_router
from app.users.router import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
