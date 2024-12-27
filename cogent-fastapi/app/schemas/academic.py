from typing import Optional, List
from pydantic import BaseModel

# Academic Department Schemas
class AcademicDepartmentBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    status: bool = True

class AcademicDepartmentCreate(AcademicDepartmentBase):
    pass

class AcademicDepartmentUpdate(AcademicDepartmentBase):
    pass

class AcademicDepartment(AcademicDepartmentBase):
    id: int

    class Config:
        from_attributes = True

# Degree Level Schemas
class DegreeLevelBase(BaseModel):
    code: str
    name: str
    duration_years: float
    status: bool = True

class DegreeLevelCreate(DegreeLevelBase):
    pass

class DegreeLevelUpdate(DegreeLevelBase):
    pass

class DegreeLevel(DegreeLevelBase):
    id: int

    class Config:
        from_attributes = True

# Degree Program Schemas
class DegreeProgramBase(BaseModel):
    academic_department_id: int
    degree_level_id: int
    code: str
    name: str
    short_name: str
    total_credits_required: int
    status: bool = True

class DegreeProgramCreate(DegreeProgramBase):
    pass

class DegreeProgramUpdate(DegreeProgramBase):
    pass

class DegreeProgram(DegreeProgramBase):
    id: int
    academic_department: AcademicDepartment
    degree_level: DegreeLevel

    class Config:
        from_attributes = True

# Subject Schemas
class SubjectBase(BaseModel):
    code: str
    name: str
    category: str
    credits: int
    lecture_hours: int
    tutorial_hours: int
    practical_hours: int
    theory_exam_duration: Optional[float] = None
    practical_exam_duration: Optional[float] = None
    is_theory: bool = True
    is_practical: bool = False
    is_elective: bool = False
    max_theory_marks: Optional[int] = None
    max_practical_marks: Optional[int] = None
    passing_marks: int
    is_semipractical: bool = False
    is_functional: bool = False
    status: bool = True

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int

    class Config:
        from_attributes = True

# Program Subject Mapping Schemas
class ProgramSubjectBase(BaseModel):
    program_id: int
    subject_id: int
    semester: int
    academic_year: int
    is_mandatory: bool = True

class ProgramSubjectCreate(ProgramSubjectBase):
    pass

class ProgramSubjectUpdate(ProgramSubjectBase):
    pass

class ProgramSubject(ProgramSubjectBase):
    id: int
    program: DegreeProgram
    subject: Subject

    class Config:
        from_attributes = True
