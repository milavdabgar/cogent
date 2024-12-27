from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_academic import (
    department,
    degree_level,
    degree_program,
    subject,
    program_subject
)
from app.schemas.academic import (
    AcademicDepartment as Department,
    AcademicDepartmentCreate as DepartmentCreate,
    AcademicDepartmentUpdate as DepartmentUpdate,
    DegreeLevel,
    DegreeLevelCreate,
    DegreeLevelUpdate,
    DegreeProgram,
    DegreeProgramCreate,
    DegreeProgramUpdate,
    Subject,
    SubjectCreate,
    SubjectUpdate,
    ProgramSubject,
    ProgramSubjectCreate,
    ProgramSubjectUpdate
)

router = APIRouter()

# Department endpoints
@router.get("/departments", response_model=List[Department])
def list_departments(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """List all departments."""
    return department.get_multi(db)

@router.post("/departments", response_model=Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    department_in: DepartmentCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Create a new department."""
    return department.create(db, obj_in=department_in)

@router.get("/departments/{department_id}", response_model=Department)
def get_department(
    department_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Get department details."""
    dept = department.get(db, id=department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.put("/departments/{department_id}", response_model=Department)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: int,
    department_in: DepartmentUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Update department."""
    dept = department.get(db, id=department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.update(db, db_obj=dept, obj_in=department_in)

@router.delete("/departments/{department_id}")
def delete_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Delete department."""
    dept = department.get(db, id=department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    department.remove(db, id=department_id)
    return {"message": "Department deleted successfully"}

# Degree Level endpoints
@router.get("/degree-levels", response_model=List[DegreeLevel])
def list_degree_levels(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """List all degree levels."""
    return degree_level.get_multi(db)

@router.post("/degree-levels", response_model=DegreeLevel)
def create_degree_level(
    *,
    db: Session = Depends(deps.get_db),
    degree_level_in: DegreeLevelCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Create a new degree level."""
    return degree_level.create(db, obj_in=degree_level_in)

@router.get("/degree-levels/{level_id}", response_model=DegreeLevel)
def get_degree_level(
    level_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Get degree level details."""
    level = degree_level.get(db, id=level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Degree level not found")
    return level

@router.put("/degree-levels/{level_id}", response_model=DegreeLevel)
def update_degree_level(
    *,
    db: Session = Depends(deps.get_db),
    level_id: int,
    degree_level_in: DegreeLevelUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Update degree level."""
    level = degree_level.get(db, id=level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Degree level not found")
    return degree_level.update(db, db_obj=level, obj_in=degree_level_in)

@router.delete("/degree-levels/{level_id}")
def delete_degree_level(
    *,
    db: Session = Depends(deps.get_db),
    level_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Delete degree level."""
    level = degree_level.get(db, id=level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Degree level not found")
    degree_level.remove(db, id=level_id)
    return {"message": "Degree level deleted successfully"}

# Degree Program endpoints
@router.get("/degree-programs", response_model=List[DegreeProgram])
def list_degree_programs(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """List all degree programs."""
    return degree_program.get_multi(db)

@router.post("/degree-programs", response_model=DegreeProgram)
def create_degree_program(
    *,
    db: Session = Depends(deps.get_db),
    program_in: DegreeProgramCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Create a new degree program."""
    return degree_program.create(db, obj_in=program_in)

@router.get("/degree-programs/{program_id}", response_model=DegreeProgram)
def get_degree_program(
    program_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Get degree program details."""
    program = degree_program.get(db, id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Degree program not found")
    return program

@router.put("/degree-programs/{program_id}", response_model=DegreeProgram)
def update_degree_program(
    *,
    db: Session = Depends(deps.get_db),
    program_id: int,
    program_in: DegreeProgramUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Update degree program."""
    program = degree_program.get(db, id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Degree program not found")
    return degree_program.update(db, db_obj=program, obj_in=program_in)

@router.delete("/degree-programs/{program_id}")
def delete_degree_program(
    *,
    db: Session = Depends(deps.get_db),
    program_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Delete degree program."""
    program = degree_program.get(db, id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Degree program not found")
    degree_program.remove(db, id=program_id)
    return {"message": "Degree program deleted successfully"}

@router.get("/degree-programs/{program_id}/subjects", response_model=List[Subject])
def get_program_subjects(
    program_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Get subjects in a degree program."""
    program = degree_program.get(db, id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Degree program not found")
    return program.subjects

# Subject endpoints
@router.get("/subjects", response_model=List[Subject])
def list_subjects(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """List all subjects."""
    return subject.get_multi(db)

@router.post("/subjects", response_model=Subject)
def create_subject(
    *,
    db: Session = Depends(deps.get_db),
    subject_in: SubjectCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Create a new subject."""
    return subject.create(db, obj_in=subject_in)

@router.get("/subjects/{subject_id}", response_model=Subject)
def get_subject(
    subject_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Get subject details."""
    subj = subject.get(db, id=subject_id)
    if not subj:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subj

@router.put("/subjects/{subject_id}", response_model=Subject)
def update_subject(
    *,
    db: Session = Depends(deps.get_db),
    subject_id: int,
    subject_in: SubjectUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Update subject."""
    subj = subject.get(db, id=subject_id)
    if not subj:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject.update(db, db_obj=subj, obj_in=subject_in)

@router.delete("/subjects/{subject_id}")
def delete_subject(
    *,
    db: Session = Depends(deps.get_db),
    subject_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Delete subject."""
    subj = subject.get(db, id=subject_id)
    if not subj:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject.remove(db, id=subject_id)
    return {"message": "Subject deleted successfully"}

# Program Subject endpoints
@router.get("/program-subjects/program/{program_id}", response_model=List[ProgramSubject])
def get_program_subject_mappings(
    program_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Get subjects mapped to a program."""
    return program_subject.get_by_program(db, program_id=program_id)

@router.post("/program-subjects", response_model=ProgramSubject)
def create_program_subject_mapping(
    *,
    db: Session = Depends(deps.get_db),
    mapping_in: ProgramSubjectCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Map subject to program."""
    return program_subject.create(db, obj_in=mapping_in)

@router.put("/program-subjects/{mapping_id}", response_model=ProgramSubject)
def update_program_subject_mapping(
    *,
    db: Session = Depends(deps.get_db),
    mapping_id: int,
    mapping_in: ProgramSubjectUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Update subject mapping."""
    mapping = program_subject.get(db, id=mapping_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Program-Subject mapping not found")
    return program_subject.update(db, db_obj=mapping, obj_in=mapping_in)

@router.delete("/program-subjects/{mapping_id}")
def delete_program_subject_mapping(
    *,
    db: Session = Depends(deps.get_db),
    mapping_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """Remove subject from program."""
    mapping = program_subject.get(db, id=mapping_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Program-Subject mapping not found")
    program_subject.remove(db, id=mapping_id)
    return {"message": "Subject removed from program successfully"}
