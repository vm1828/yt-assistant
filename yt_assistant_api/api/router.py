from fastapi import APIRouter
from api.routes import account

api_router = APIRouter()

api_router.include_router(account.router, prefix="/accounts", tags=["accounts"])
