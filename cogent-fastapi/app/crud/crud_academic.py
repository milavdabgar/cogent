from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.academic import (
    AcademicDepartment, DegreeLevel, DegreeProgram,
    Subject, ProgramSubject
)
from app.schemas.academic import (
    AcademicDepartmentCreate, AcademicDepartmentUpdate,
    DegreeLevelCreate, DegreeLevelUpdate,
    DegreeProgramCreate, DegreeProgramUpdate,
    SubjectCreate, SubjectUpdate,
    ProgramSubjectCreate, ProgramSubjectUpdate
)

class CRUDAcademicDepartment(CRUDBase[AcademicDepartment, AcademicDepartmentCreate, AcademicDepartmentUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[AcademicDepartment]:
        return db.query(AcademicDepartment).filter(AcademicDepartment.code == code).first()

class CRUDDegreeLevel(CRUDBase[DegreeLevel, DegreeLevelCreate, DegreeLevelUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[DegreeLevel]:
        return db.query(DegreeLevel).filter(DegreeLevel.code == code).first()

class CRUDDegreeProgram(CRUDBase[DegreeProgram, DegreeProgramCreate, DegreeProgramUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[DegreeProgram]:
        return db.query(DegreeProgram).filter(DegreeProgram.code == code).first()

    def get_by_department(
        self, db: Session, *, department_id: int, skip: int = 0, limit: int = 100
    ) -> List[DegreeProgram]:
        return db.query(DegreeProgram)\
            .filter(DegreeProgram.department_id == department_id)\
            .offset(skip)\
            .limit(limit)\
            .all()

class CRUDSubject(CRUDBase[Subject, SubjectCreate, SubjectUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Subject]:
        return db.query(Subject).filter(Subject.code == code).first()

class CRUDProgramSubject(CRUDBase[ProgramSubject, ProgramSubjectCreate, ProgramSubjectUpdate]):
    def get_by_program(
        self, db: Session, *, program_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProgramSubject]:
        return db.query(ProgramSubject)\
            .filter(ProgramSubject.program_id == program_id)\
            .offset(skip)\
            .limit(limit)\
            .all()

department = CRUDAcademicDepartment(AcademicDepartment)
degree_level = CRUDDegreeLevel(DegreeLevel)
degree_program = CRUDDegreeProgram(DegreeProgram)
subject = CRUDSubject(Subject)
program_subject = CRUDProgramSubject(ProgramSubject)
