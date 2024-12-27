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

class FacultyCourseAssignmentBase(BaseModel):
    faculty_id: int
    course_id: int
    academic_year: str
    semester: int
    is_active: bool = True

class FacultyCourseAssignmentCreate(FacultyCourseAssignmentBase):
    pass

class FacultyCourseAssignmentUpdate(BaseModel):
    academic_year: Optional[str] = None
    semester: Optional[int] = None
    is_active: Optional[bool] = None

class FacultyCourseAssignmentResponse(FacultyCourseAssignmentBase):
    id: int
    
    class Config:
        from_attributes = True

class CourseResponse(CourseBase):
    id: int
    faculty_assignments: List[FacultyCourseAssignmentResponse] = []
    
    class Config:
        from_attributes = True
