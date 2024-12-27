from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.models.college import College
from app.models.course import Course
from app.schemas.user import UserCreate, UserUpdate

def get_user(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[User]:
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if search:
        search_filter = (
            User.email.ilike(f"%{search}%") |
            User.first_name.ilike(f"%{search}%") |
            User.last_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        hashed_password=get_password_hash(obj_in.password),
        role=obj_in.role,
        phone_number=obj_in.phone_number,
        date_of_birth=obj_in.date_of_birth
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_user(
    db: Session,
    db_obj: User,
    obj_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        if field == "password":
            setattr(db_obj, "hashed_password", get_password_hash(update_data["password"]))
        else:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Admin specific operations
def count_total_users(db: Session) -> int:
    return db.query(func.count(User.id)).scalar()

def count_total_colleges(db: Session) -> int:
    return db.query(func.count(College.id)).scalar()

def count_active_students(db: Session) -> int:
    return db.query(func.count(User.id)).filter(
        User.role == UserRole.STUDENT,
        User.is_active == True
    ).scalar()

def count_active_faculty(db: Session) -> int:
    return db.query(func.count(User.id)).filter(
        User.role == UserRole.FACULTY,
        User.is_active == True
    ).scalar()

def count_total_courses(db: Session) -> int:
    return db.query(func.count(Course.id)).scalar()

def count_total_labs(db: Session) -> int:
    return db.query(func.count(Course.id)).filter(
        Course.type == 'practical'
    ).scalar()
