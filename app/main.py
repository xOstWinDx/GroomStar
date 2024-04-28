from fastapi import FastAPI, Query

from app.auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
