from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from app.models.course import Course, FacultyCourseAssignment
from app.schemas.course import CourseCreate, CourseUpdate, FacultyAssignmentCreate, FacultyAssignmentUpdate

def get_course(db: Session, course_id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == course_id).first()

def get_course_by_code(db: Session, code: str) -> Optional[Course]:
    return db.query(Course).filter(Course.code == code).first()

def get_courses(
    db: Session,
    department_id: Optional[int] = None,
    semester: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Course]:
    query = db.query(Course)
    
    if department_id:
        query = query.filter(Course.department_id == department_id)
    
    if semester:
        query = query.filter(Course.semester == semester)
    
    if search:
        search_filter = (
            Course.name.ilike(f"%{search}%") |
            Course.code.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()

def create_course(db: Session, course: CourseCreate) -> Course:
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(
    db: Session,
    db_obj: Course,
    obj_in: Union[CourseUpdate, Dict[str, Any]]
) -> Course:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_course(db: Session, course_id: int) -> Course:
    course = get_course(db, course_id)
    if course:
        course.is_active = False
        db.add(course)
        db.commit()
        db.refresh(course)
    return course

# Faculty Course Assignment operations
def get_faculty_assignment(db: Session, assignment_id: int) -> Optional[FacultyCourseAssignment]:
    return db.query(FacultyCourseAssignment).filter(FacultyCourseAssignment.id == assignment_id).first()

def get_faculty_assignments(
    db: Session,
    faculty_id: Optional[int] = None,
    course_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    semester: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[FacultyCourseAssignment]:
    query = db.query(FacultyCourseAssignment)
    
    if faculty_id:
        query = query.filter(FacultyCourseAssignment.faculty_id == faculty_id)
    
    if course_id:
        query = query.filter(FacultyCourseAssignment.course_id == course_id)
    
    if academic_year:
        query = query.filter(FacultyCourseAssignment.academic_year == academic_year)
    
    if semester:
        query = query.filter(FacultyCourseAssignment.semester == semester)
    
    return query.offset(skip).limit(limit).all()

def create_faculty_assignment(db: Session, assignment: FacultyAssignmentCreate) -> FacultyCourseAssignment:
    db_assignment = FacultyCourseAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def update_faculty_assignment(
    db: Session,
    db_obj: FacultyCourseAssignment,
    obj_in: Union[FacultyAssignmentUpdate, Dict[str, Any]]
) -> FacultyCourseAssignment:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_faculty_assignment(db: Session, assignment_id: int) -> FacultyCourseAssignment:
    assignment = get_faculty_assignment(db, assignment_id)
    if assignment:
        assignment.is_active = False
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
    return assignment
