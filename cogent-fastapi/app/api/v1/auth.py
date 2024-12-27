from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.crud.crud_user import user as user_crud
from app.schemas.user import Token, UserCreate, UserResponse, UserLogin
from app.schemas.profile import (
    ProfileUpdate,
    ProfileResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)
from app.api import deps
from app.core.security import get_password_hash
from app.models.user import User, UserRole, StudentDetails, FacultyDetails, HODDetails, LabAssistantDetails, PrincipalDetails

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """
    Create new user with role-specific details.
    """
    new_user = user_crud.create(db, user_in)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    *,
    db: Session = Depends(get_db),
    login_data: UserLogin
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    authenticated_user = user_crud.authenticate(db=db, email=login_data.email, password=login_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify role if provided
    if login_data.role and authenticated_user.role != login_data.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect role for this user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={
            "sub": str(authenticated_user.id),  # Use user ID instead of email
            "email": authenticated_user.email,
            "role": authenticated_user.role
        },
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/profile/me", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get current user profile."""
    # Ensure role-specific details are loaded
    if current_user.role == UserRole.STUDENT and current_user.student_details:
        db.refresh(current_user.student_details)
    elif current_user.role == UserRole.FACULTY and current_user.faculty_details:
        db.refresh(current_user.faculty_details)
    elif current_user.role == UserRole.HOD and current_user.hod_details:
        db.refresh(current_user.hod_details)
    elif current_user.role == UserRole.PRINCIPAL and current_user.principal_details:
        db.refresh(current_user.principal_details)
    elif current_user.role == UserRole.LAB_ASSISTANT and current_user.lab_assistant_details:
        db.refresh(current_user.lab_assistant_details)
    
    return current_user

@router.put("/profile/me", response_model=ProfileResponse)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """Update current user profile."""
    # Update basic user fields
    update_data = profile_update.dict(exclude_unset=True)
    
    # Handle basic fields
    basic_fields = ['email', 'first_name', 'last_name', 'phone_number', 'date_of_birth']
    for field in basic_fields:
        if field in update_data:
            setattr(current_user, field, update_data[field])
    
    # Handle role-specific details
    if current_user.role == UserRole.STUDENT:
        if not current_user.student_details:
            current_user.student_details = StudentDetails(user_id=current_user.id)
            db.add(current_user.student_details)
            
        if profile_update.student_details:
            student_details = update_data.get('student_details', {})
            for field, value in student_details.items():
                setattr(current_user.student_details, field, value)
    
    elif current_user.role == UserRole.FACULTY:
        if not current_user.faculty_details:
            current_user.faculty_details = FacultyDetails(user_id=current_user.id)
            db.add(current_user.faculty_details)
            
        if profile_update.faculty_details:
            faculty_details = update_data.get('faculty_details', {})
            for field, value in faculty_details.items():
                setattr(current_user.faculty_details, field, value)
    
    elif current_user.role == UserRole.HOD:
        if not current_user.hod_details:
            current_user.hod_details = HODDetails(user_id=current_user.id)
            db.add(current_user.hod_details)
            
        if profile_update.hod_details:
            hod_details = update_data.get('hod_details', {})
            for field, value in hod_details.items():
                setattr(current_user.hod_details, field, value)
    
    elif current_user.role == UserRole.PRINCIPAL:
        if not current_user.principal_details:
            current_user.principal_details = PrincipalDetails(user_id=current_user.id)
            db.add(current_user.principal_details)
            
        if profile_update.principal_details:
            principal_details = update_data.get('principal_details', {})
            for field, value in principal_details.items():
                setattr(current_user.principal_details, field, value)
    
    elif current_user.role == UserRole.LAB_ASSISTANT:
        if not current_user.lab_assistant_details:
            current_user.lab_assistant_details = LabAssistantDetails(user_id=current_user.id)
            db.add(current_user.lab_assistant_details)
            
        if profile_update.lab_assistant_details:
            lab_assistant_details = update_data.get('lab_assistant_details', {})
            for field, value in lab_assistant_details.items():
                setattr(current_user.lab_assistant_details, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/profile/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """Change current user password."""
    if not security.verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    current_user.hashed_password = get_password_hash(password_change.new_password)
    db.add(current_user)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/profile/reset-password")
async def reset_password(
    password_reset: PasswordReset,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Request password reset."""
    user_obj = user_crud.get_by_email(db, email=password_reset.email)
    if user_obj:
        # TODO: Send password reset email
        pass
    return {"message": "If your email is registered, you will receive a password reset link"}

@router.post("/profile/reset-password/confirm")
async def reset_password_confirm(
    password_reset: PasswordResetConfirm,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Confirm password reset."""
    # TODO: Implement password reset confirmation
    return {"message": "Password reset successfully"}
