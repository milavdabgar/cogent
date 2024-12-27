from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from app.models.college import College, Department
from app.schemas.college import CollegeCreate, CollegeUpdate, DepartmentCreate, DepartmentUpdate

def get_college(db: Session, college_id: int) -> Optional[College]:
    return db.query(College).filter(College.id == college_id).first()

def get_college_by_code(db: Session, code: str) -> Optional[College]:
    return db.query(College).filter(College.code == code).first()

def get_colleges(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[College]:
    query = db.query(College)
    if search:
        search_filter = (
            College.name.ilike(f"%{search}%") |
            College.code.ilike(f"%{search}%") |
            College.city.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()

def create_college(db: Session, college: CollegeCreate) -> College:
    db_college = College(**college.dict())
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college

def update_college(
    db: Session,
    db_obj: College,
    obj_in: Union[CollegeUpdate, Dict[str, Any]]
) -> College:
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

def delete_college(db: Session, college_id: int) -> College:
    college = get_college(db, college_id)
    if college:
        college.is_active = False
        db.add(college)
        db.commit()
        db.refresh(college)
    return college

# Department operations
def get_department(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()

def get_departments(
    db: Session,
    college_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Department]:
    query = db.query(Department)
    if college_id:
        query = query.filter(Department.college_id == college_id)
    return query.offset(skip).limit(limit).all()

def create_department(db: Session, department: DepartmentCreate) -> Department:
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(
    db: Session,
    db_obj: Department,
    obj_in: Union[DepartmentUpdate, Dict[str, Any]]
) -> Department:
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

def delete_department(db: Session, department_id: int) -> Department:
    department = get_department(db, department_id)
    if department:
        department.is_active = False
        db.add(department)
        db.commit()
        db.refresh(department)
    return department
