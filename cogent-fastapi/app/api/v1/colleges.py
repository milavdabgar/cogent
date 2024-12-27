from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_college
from app.schemas import college as college_schemas
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[college_schemas.College])
def get_colleges(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):
    """
    Get list of colleges.
    """
    colleges = crud_college.get_colleges(db, skip=skip, limit=limit, search=search)
    return colleges

@router.post("/", response_model=college_schemas.College)
def create_college(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    college_in: college_schemas.CollegeCreate
):
    """
    Create new college.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    college = crud_college.get_college_by_code(db, code=college_in.code)
    if college:
        raise HTTPException(
            status_code=400,
            detail="A college with this code already exists"
        )
    
    college = crud_college.create_college(db, college=college_in)
    return college

@router.get("/{college_id}", response_model=college_schemas.College)
def get_college(
    college_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Get college by ID.
    """
    college = crud_college.get_college(db, college_id=college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return college

@router.put("/{college_id}", response_model=college_schemas.College)
def update_college(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    college_id: int,
    college_in: college_schemas.CollegeUpdate
):
    """
    Update college.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    college = crud_college.get_college(db, college_id=college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    # Check if code is being updated and if it already exists
    if college_in.code and college_in.code != college.code:
        existing_college = crud_college.get_college_by_code(db, code=college_in.code)
        if existing_college:
            raise HTTPException(
                status_code=400,
                detail="A college with this code already exists"
            )
    
    college = crud_college.update_college(db, db_obj=college, obj_in=college_in)
    return college

@router.delete("/{college_id}")
def delete_college(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    college_id: int
):
    """
    Delete college.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    college = crud_college.get_college(db, college_id=college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    college = crud_college.delete_college(db, college_id=college_id)
    return {"message": "College successfully deactivated"}

# Department endpoints
@router.get("/departments/", response_model=List[college_schemas.Department])
def get_departments(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    college_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get list of departments.
    """
    departments = crud_college.get_departments(
        db, college_id=college_id, skip=skip, limit=limit
    )
    return departments

@router.post("/departments/", response_model=college_schemas.Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    department_in: college_schemas.DepartmentCreate
):
    """
    Create new department.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    department = crud_college.create_department(db, department=department_in)
    return department

@router.put("/departments/{department_id}", response_model=college_schemas.Department)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    department_id: int,
    department_in: college_schemas.DepartmentUpdate
):
    """
    Update department.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    department = crud_college.get_department(db, department_id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    department = crud_college.update_department(
        db, db_obj=department, obj_in=department_in
    )
    return department

@router.delete("/departments/{department_id}")
def delete_department(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    department_id: int
):
    """
    Delete department.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    department = crud_college.get_department(db, department_id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    department = crud_college.delete_department(db, department_id=department_id)
    return {"message": "Department successfully deactivated"}
