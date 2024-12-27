from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import User
from app.schemas.college import CollegeResponse, CollegeCreate, CollegeUpdate
from app.crud import college as college_crud

router = APIRouter()

@router.get("/colleges", response_model=List[CollegeResponse])
async def get_colleges(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_dte_admin),
    db: Session = Depends(deps.get_db),
):
    """Get all colleges"""
    colleges = college_crud.get_multi(
        db, skip=skip, limit=limit, search=search
    )
    return colleges

@router.post("/colleges", response_model=CollegeResponse)
async def create_college(
    college: CollegeCreate,
    current_user: User = Depends(deps.get_current_active_dte_admin),
    db: Session = Depends(deps.get_db),
):
    """Create a new college"""
    college = college_crud.create(db, obj_in=college)
    return college

@router.put("/colleges/{college_id}", response_model=CollegeResponse)
async def update_college(
    college_id: int,
    college: CollegeUpdate,
    current_user: User = Depends(deps.get_current_active_dte_admin),
    db: Session = Depends(deps.get_db),
):
    """Update a college"""
    db_college = college_crud.get(db, id=college_id)
    if not db_college:
        raise HTTPException(status_code=404, detail="College not found")
    college = college_crud.update(db, db_obj=db_college, obj_in=college)
    return college

@router.delete("/colleges/{college_id}")
async def delete_college(
    college_id: int,
    current_user: User = Depends(deps.get_current_active_dte_admin),
    db: Session = Depends(deps.get_db),
):
    """Delete a college"""
    db_college = college_crud.get(db, id=college_id)
    if not db_college:
        raise HTTPException(status_code=404, detail="College not found")
    college = college_crud.remove(db, id=college_id)
    return {"status": "success"}
