from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from .user import UserRole

class StudentDetails(BaseModel):
    enrollment_number: Optional[str] = None
    current_semester: Optional[int] = None
    department: Optional[str] = None
    
    class Config:
        from_attributes = True

class FacultyDetails(BaseModel):
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    date_of_joining: Optional[date] = None
    experience_years: Optional[int] = None
    
    class Config:
        from_attributes = True

class HODDetails(BaseModel):
    department: Optional[str] = None
    qualification: Optional[str] = None
    date_of_joining: Optional[date] = None
    experience_years: Optional[int] = None
    
    class Config:
        from_attributes = True

class LabAssistantDetails(BaseModel):
    department: Optional[str] = None
    lab_type: Optional[str] = None
    date_of_joining: Optional[date] = None
    
    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    # Role specific fields
    student_details: Optional[StudentDetails] = None
    faculty_details: Optional[FacultyDetails] = None
    hod_details: Optional[HODDetails] = None
    lab_assistant_details: Optional[LabAssistantDetails] = None
    
    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    confirm_password: str

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    role: UserRole
    
    # Role specific details as nested models
    student_details: Optional[StudentDetails] = None
    faculty_details: Optional[FacultyDetails] = None
    hod_details: Optional[HODDetails] = None
    lab_assistant_details: Optional[LabAssistantDetails] = None
    
    class Config:
        from_attributes = True
