from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from app.core.security import get_current_user, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User, UserRole, StudentDetails, FacultyDetails, HODDetails, LabAssistantDetails, PrincipalDetails
from app.schemas.profile import (
    ProfileUpdate,
    ProfileResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)
from app.core.config import settings

router = APIRouter()

@router.get("/me", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
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

@router.put("/me", response_model=ProfileResponse)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
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

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Change current user password."""
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    if password_change.new_password != password_change.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    current_user.hashed_password = get_password_hash(password_change.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    password_reset: PasswordReset,
    db: Session = Depends(get_db)
) -> Any:
    """Request password reset."""
    user = db.query(User).filter(User.email == password_reset.email).first()
    if not user:
        # Return success even if user doesn't exist to prevent email enumeration
        return {"message": "If the email exists, a password reset link will be sent"}
    
    # TODO: Implement email sending logic
    # For now, just return success message
    return {"message": "If the email exists, a password reset link will be sent"}

@router.post("/reset-password-confirm", status_code=status.HTTP_200_OK)
async def reset_password_confirm(
    password_reset: PasswordResetConfirm,
    db: Session = Depends(get_db)
) -> Any:
    """Confirm password reset."""
    # TODO: Implement token verification logic
    if password_reset.new_password != password_reset.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # TODO: Implement password reset logic
    return {"message": "Password reset successfully"}
