from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_users(
        self,
        db: Session,
        *,
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
            search_term = f"%{search}%"
            query = query.filter(
                (User.email.ilike(search_term)) |
                (User.first_name.ilike(search_term)) |
                (User.last_name.ilike(search_term))
            )
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            phone_number=obj_in.phone_number,
            date_of_birth=obj_in.date_of_birth,
            role=obj_in.role,
            is_active=True,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    # Admin specific operations
    def count_total_users(self, db: Session) -> int:
        """Count total users"""
        return db.query(User).count()

    def count_active_students(self, db: Session) -> int:
        """Count active students"""
        return db.query(User)\
            .filter(User.role == "student")\
            .filter(User.is_active == True)\
            .count()

    def count_active_faculty(self, db: Session) -> int:
        """Count active faculty"""
        return db.query(User)\
            .filter(User.role == "faculty")\
            .filter(User.is_active == True)\
            .count()

user = CRUDUser(User)
