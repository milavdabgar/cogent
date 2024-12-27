from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_course
from app.schemas import course as course_schemas
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[course_schemas.CourseResponse])
def get_courses(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    department_id: Optional[int] = None,
    semester: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):
    """
    Get list of courses.
    """
    return crud_course.get_courses(
        db,
        department_id=department_id,
        semester=semester,
        skip=skip,
        limit=limit,
        search=search
    )

@router.post("/", response_model=course_schemas.CourseResponse)
def create_course(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    course_in: course_schemas.CourseCreate
):
    """
    Create new course.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DTE_ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to create course"
        )
    return crud_course.create_course(db, course=course_in)

@router.get("/{course_id}", response_model=course_schemas.CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Get course by ID.
    """
    course = crud_course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=course_schemas.CourseResponse)
def update_course(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    course_id: int,
    course_in: course_schemas.CourseUpdate
):
    """
    Update course.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DTE_ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to update course"
        )
    course = crud_course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud_course.update_course(db, db_obj=course, obj_in=course_in)

@router.delete("/{course_id}")
def delete_course(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    course_id: int
):
    """
    Delete course.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DTE_ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to delete course"
        )
    course = crud_course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    crud_course.delete_course(db, course_id=course_id)
    return {"message": "Course deleted successfully"}

# Faculty Course Assignment endpoints
@router.get("/faculty-assignments", response_model=List[course_schemas.FacultyCourseAssignmentResponse])
def get_faculty_assignments(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    faculty_id: Optional[int] = None,
    course_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    semester: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get list of faculty course assignments.
    """
    return crud_course.get_faculty_assignments(
        db,
        faculty_id=faculty_id,
        course_id=course_id,
        academic_year=academic_year,
        semester=semester,
        skip=skip,
        limit=limit
    )

@router.post("/faculty-assignments", response_model=course_schemas.FacultyCourseAssignmentResponse)
def create_faculty_assignment(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    assignment_in: course_schemas.FacultyCourseAssignmentCreate
):
    """
    Create new faculty course assignment.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DTE_ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to create faculty assignment"
        )
    return crud_course.create_faculty_assignment(db, assignment=assignment_in)

@router.put("/faculty-assignments/{assignment_id}", response_model=course_schemas.FacultyCourseAssignmentResponse)
def update_faculty_assignment(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    assignment_id: int,
    assignment_in: course_schemas.FacultyCourseAssignmentUpdate
):
    """
    Update faculty course assignment.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DTE_ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to update faculty assignment"
        )
    assignment = crud_course.get_faculty_assignment(db, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Faculty assignment not found")
    return crud_course.update_faculty_assignment(db, db_obj=assignment, obj_in=assignment_in)

@router.delete("/faculty-assignments/{assignment_id}")
def delete_faculty_assignment(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    assignment_id: int
):
    """
    Delete faculty course assignment.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DTE_ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to delete faculty assignment"
        )
    assignment = crud_course.get_faculty_assignment(db, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Faculty assignment not found")
    crud_course.delete_faculty_assignment(db, assignment_id=assignment_id)
    return {"message": "Faculty assignment deleted successfully"}
