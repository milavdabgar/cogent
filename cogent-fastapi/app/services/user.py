from sqlalchemy.orm import Session
from app.models.user import User, PrincipalDetails, HODDetails, FacultyDetails, LabAssistantDetails, StudentDetails, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    # Check if user exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        role=user.role
    )
    db.add(db_user)
    db.flush()  # Get the user ID without committing

    # Create role-specific details
    if user.role == UserRole.PRINCIPAL and user.principal_details:
        db_details = PrincipalDetails(**user.principal_details.dict(), user_id=db_user.id)
        db.add(db_details)
    elif user.role == UserRole.HOD and user.hod_details:
        db_details = HODDetails(**user.hod_details.dict(), user_id=db_user.id)
        db.add(db_details)
    elif user.role == UserRole.FACULTY and user.faculty_details:
        db_details = FacultyDetails(**user.faculty_details.dict(), user_id=db_user.id)
        db.add(db_details)
    elif user.role == UserRole.LAB_ASSISTANT and user.lab_assistant_details:
        db_details = LabAssistantDetails(**user.lab_assistant_details.dict(), user_id=db_user.id)
        db.add(db_details)
    elif user.role == UserRole.STUDENT and user.student_details:
        db_details = StudentDetails(**user.student_details.dict(), user_id=db_user.id)
        db.add(db_details)

    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
