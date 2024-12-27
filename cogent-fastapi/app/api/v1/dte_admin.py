from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import User
from app.schemas.college import (
    CollegeResponse, CollegeCreate, CollegeUpdate,
    DepartmentResponse, DepartmentCreate, DepartmentUpdate
)
from app.crud import college as college_crud

router = APIRouter()

@router.get("/colleges", response_model=List[CollegeResponse])
async def get_colleges(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Get all colleges"""
    colleges = college_crud.get_colleges(
        db, skip=skip, limit=limit, search=search
    )
    return colleges

@router.post("/colleges", response_model=CollegeResponse)
async def create_college(
    college: CollegeCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Create a new college"""
    college = college_crud.create_college(db, college=college)
    return college

@router.put("/colleges/{college_id}", response_model=CollegeResponse)
async def update_college(
    college_id: int,
    college: CollegeUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Update a college"""
    db_college = college_crud.update_college(db, college_id=college_id, college=college)
    if not db_college:
        raise HTTPException(status_code=404, detail="College not found")
    return db_college

@router.delete("/colleges/{college_id}")
async def delete_college(
    college_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Delete a college"""
    success = college_crud.delete_college(db, college_id=college_id)
    if not success:
        raise HTTPException(status_code=404, detail="College not found")
    return {"message": "College deleted successfully"}

@router.get("/colleges/{college_id}", response_model=CollegeResponse)
async def get_college(
    college_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Get a specific college"""
    college = college_crud.get_college(db, college_id=college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return college

@router.get("/colleges/{college_id}/departments", response_model=List[DepartmentResponse])
async def get_college_departments(
    college_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Get departments of a specific college"""
    college = college_crud.get_college(db, college_id=college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    departments = college_crud.get_departments(
        db, college_id=college_id, skip=skip, limit=limit
    )
    return departments

@router.get("/departments", response_model=List[DepartmentResponse])
async def get_departments(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Get all departments"""
    departments = college_crud.get_all_departments(
        db, skip=skip, limit=limit, search=search
    )
    return departments

@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Create a new department"""
    # Check if college exists
    college = college_crud.get_college(db, college_id=department.college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    # Create department
    department = college_crud.create_department(db, department=department)
    return department

@router.put("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department: DepartmentUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Update a department"""
    # Check if department exists
    db_department = college_crud.get_department(db, department_id=department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Update department
    department = college_crud.update_department(
        db, department_id=department_id, department=department
    )
    return department

@router.delete("/departments/{department_id}")
async def delete_department(
    department_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """Delete a department"""
    # Check if department exists
    success = college_crud.delete_department(db, department_id=department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department deleted successfully"}
