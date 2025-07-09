from fastapi import FastAPI
from src.core.api.v1.endpoints.auth.register import router as user_router
from src.core.api.v1.endpoints.auth.login import router as user_login_router

app = FastAPI()

app.include_router(user_router)
app.include_router(user_login_router)
