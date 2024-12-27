from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.college import College, Department
from app.schemas.college import CollegeCreate, CollegeUpdate, DepartmentCreate, DepartmentUpdate

def get_college(db: Session, college_id: int) -> Optional[College]:
    return db.query(College).filter(College.id == college_id).first()

def get_colleges(
    db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None
) -> List[College]:
    query = db.query(College)
    if search:
        search_filter = or_(
            College.name.ilike(f"%{search}%"),
            College.code.ilike(f"%{search}%"),
            College.address.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()

def create_college(db: Session, college: CollegeCreate) -> College:
    db_college = College(**college.dict())
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college

def update_college(db: Session, college_id: int, college: CollegeUpdate) -> Optional[College]:
    db_college = get_college(db, college_id)
    if not db_college:
        return None
    
    for field, value in college.dict(exclude_unset=True).items():
        setattr(db_college, field, value)
    
    db.commit()
    db.refresh(db_college)
    return db_college

def delete_college(db: Session, college_id: int) -> bool:
    db_college = get_college(db, college_id)
    if not db_college:
        return False
    
    db.delete(db_college)
    db.commit()
    return True

def get_department(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()

def get_all_departments(
    db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None
) -> List[Department]:
    query = db.query(Department)
    if search:
        search_filter = or_(
            Department.name.ilike(f"%{search}%"),
            Department.code.ilike(f"%{search}%"),
            Department.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()

def get_departments(
    db: Session, college_id: int, skip: int = 0, limit: int = 100
) -> List[Department]:
    return db.query(Department)\
        .filter(Department.college_id == college_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_department(db: Session, department: DepartmentCreate) -> Department:
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(
    db: Session, department_id: int, department: DepartmentUpdate
) -> Optional[Department]:
    db_department = get_department(db, department_id)
    if not db_department:
        return None
    
    for field, value in department.dict(exclude_unset=True).items():
        setattr(db_department, field, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: int) -> bool:
    db_department = get_department(db, department_id)
    if not db_department:
        return False
    
    db.delete(db_department)
    db.commit()
    return True
