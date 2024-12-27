from fastapi import APIRouter
from app.api.v1 import (
    auth,
    admin,
    dte_admin,
    profile,
    colleges,
    courses,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(dte_admin.router, prefix="/dte-admin", tags=["dte-admin"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(colleges.router, prefix="/colleges", tags=["colleges"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
