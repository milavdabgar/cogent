from typing import Optional, List
from pydantic import BaseModel
from app.models.course import CourseType

class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    type: CourseType
    semester: int
    department_id: int
    is_active: bool = True

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    credits: Optional[int] = None
    type: Optional[CourseType] = None
    semester: Optional[int] = None
    is_active: Optional[bool] = None

class FacultyAssignmentBase(BaseModel):
    faculty_id: int
    course_id: int
    academic_year: str
    semester: int
    is_active: bool = True

class FacultyAssignmentCreate(FacultyAssignmentBase):
    pass

class FacultyAssignmentUpdate(BaseModel):
    academic_year: Optional[str] = None
    semester: Optional[int] = None
    is_active: Optional[bool] = None

class FacultyAssignment(FacultyAssignmentBase):
    id: int
    
    class Config:
        orm_mode = True

class Course(CourseBase):
    id: int
    faculty_assignments: List[FacultyAssignment] = []
    
    class Config:
        orm_mode = True
