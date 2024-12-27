from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_user
from app.schemas import admin as admin_schemas
from app.core.security import get_password_hash
from app.models.user import UserRole
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats", response_model=admin_schemas.AdminStats)
def get_admin_stats(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user)
):
    """
    Get admin dashboard statistics
    """
    # Get stats from database
    total_users = crud_user.count_total_users(db)
    active_students = crud_user.count_active_students(db)
    active_faculty = crud_user.count_active_faculty(db)
    
    return {
        "total_users": total_users,
        "active_students": active_students,
        "active_faculty": active_faculty
    }

@router.get("/users", response_model=List[admin_schemas.UserInDB])
def get_users(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user),
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """
    Get list of users with optional filtering
    """
    users = crud_user.get_users(
        db,
        skip=skip,
        limit=limit,
        role=role,
        search=search,
        is_active=is_active
    )
    return users

@router.post("/users", response_model=admin_schemas.UserInDB)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user),
    user_in: admin_schemas.UserCreate
):
    """
    Create new user
    """
    # Check if user with this email exists
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )
    
    user = crud_user.create_user(db, obj_in=user_in)
    return user

@router.put("/users/{user_id}", response_model=admin_schemas.UserInDB)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user),
    user_id: int,
    user_in: admin_schemas.UserUpdate
):
    """
    Update user
    """
    user = crud_user.get_user(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = crud_user.update_user(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/users/{user_id}")
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user),
    user_id: int
):
    """
    Delete user
    """
    user = crud_user.get_user(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Instead of hard delete, we'll just deactivate the user
    user = crud_user.update_user(db, db_obj=user, obj_in={"is_active": False})
    return {"message": "User successfully deactivated"}

@router.get("/system-health", response_model=List[admin_schemas.SystemHealth])
def get_system_health(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user)
):
    """
    Get system health status
    """
    # In a real application, you would check actual services
    # This is just a mock implementation
    return [
        {
            "service_name": "Authentication Service",
            "status": "Operational",
            "uptime": 99.9,
            "last_check": datetime.now().date()
        },
        {
            "service_name": "Database",
            "status": "Operational",
            "uptime": 99.8,
            "last_check": datetime.now().date()
        },
        {
            "service_name": "File Storage",
            "status": "Operational",
            "uptime": 99.9,
            "last_check": datetime.now().date()
        }
    ]

@router.get("/recent-activities", response_model=List[admin_schemas.RecentActivity])
def get_recent_activities(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user),
    limit: int = Query(10, le=50)
):
    """
    Get recent system activities
    """
    # In a real application, you would fetch this from an activity log table
    # This is just a mock implementation
    return [
        {
            "id": 1,
            "action": "USER_CREATED",
            "description": "New user account created",
            "timestamp": datetime.now().date(),
            "user_id": 1,
            "user_email": "user@example.com"
        }
    ]
