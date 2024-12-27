from fastapi import APIRouter

from app.api.v1 import (
    auth,
    admin,
    dte_admin,
    gtu_admin
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(dte_admin.router, prefix="/dte-admin", tags=["dte-admin"])
api_router.include_router(gtu_admin.router, prefix="/gtu-admin", tags=["gtu-admin"])
