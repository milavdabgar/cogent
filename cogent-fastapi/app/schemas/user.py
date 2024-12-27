from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    date_of_birth: date
    role: UserRole

class PrincipalDetailsBase(BaseModel):
    date_of_joining: date
    qualification: str
    experience_years: int

class HODDetailsBase(BaseModel):
    department: str
    date_of_joining: date
    qualification: str
    experience_years: int

class FacultyDetailsBase(BaseModel):
    department: str
    date_of_joining: date
    qualification: str
    specialization: str

class LabAssistantDetailsBase(BaseModel):
    department: str
    date_of_joining: date
    lab_type: str

class StudentDetailsBase(BaseModel):
    enrollment_number: str
    department: str
    date_of_admission: date
    current_semester: int

class DTEAdminDetailsBase(BaseModel):
    jurisdiction: str
    date_of_joining: date
    access_level: str

class AdminDetailsBase(BaseModel):
    super_admin: bool = False
    date_of_joining: date
    access_level: str

class UserCreate(UserBase):
    password: str
    dte_admin_details: Optional[DTEAdminDetailsBase] = None
    admin_details: Optional[AdminDetailsBase] = None
    principal_details: Optional[PrincipalDetailsBase] = None
    hod_details: Optional[HODDetailsBase] = None
    faculty_details: Optional[FacultyDetailsBase] = None
    lab_assistant_details: Optional[LabAssistantDetailsBase] = None
    student_details: Optional[StudentDetailsBase] = None

    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('student_details', always=True)
    def validate_student_details(cls, v, values):
        if values.get('role') == UserRole.STUDENT and not v:
            raise ValueError('Student role requires student details')
        return v

    @validator('principal_details', always=True)
    def validate_principal_details(cls, v, values):
        if values.get('role') == UserRole.PRINCIPAL and not v:
            raise ValueError('Principal role requires principal details')
        return v

    @validator('hod_details', always=True)
    def validate_hod_details(cls, v, values):
        if values.get('role') == UserRole.HOD and not v:
            raise ValueError('HOD role requires HOD details')
        return v

    @validator('faculty_details', always=True)
    def validate_faculty_details(cls, v, values):
        if values.get('role') == UserRole.FACULTY and not v:
            raise ValueError('Faculty role requires faculty details')
        return v

    @validator('lab_assistant_details', always=True)
    def validate_lab_assistant_details(cls, v, values):
        if values.get('role') == UserRole.LAB_ASSISTANT and not v:
            raise ValueError('Lab Assistant role requires lab assistant details')
        return v

    @validator('dte_admin_details', always=True)
    def validate_dte_admin_details(cls, v, values):
        if values.get('role') == UserRole.DTE_ADMIN and not v:
            raise ValueError('DTE Admin role requires DTE Admin details')
        return v

    @validator('admin_details', always=True)
    def validate_admin_details(cls, v, values):
        if values.get('role') == UserRole.ADMIN and not v:
            raise ValueError('Admin role requires Admin details')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None

    @validator('role')
    def validate_role(cls, v):
        if v:
            try:
                role_key = v.replace(' ', '_').upper()
                return UserRole[role_key]
            except KeyError:
                raise ValueError('Invalid role')
        return None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    role: UserRole

class UserResponse(UserBase):
    id: int
    is_active: bool
    principal_details: Optional[PrincipalDetailsBase] = None
    hod_details: Optional[HODDetailsBase] = None
    faculty_details: Optional[FacultyDetailsBase] = None
    lab_assistant_details: Optional[LabAssistantDetailsBase] = None
    student_details: Optional[StudentDetailsBase] = None
    dte_admin_details: Optional[DTEAdminDetailsBase] = None
    admin_details: Optional[AdminDetailsBase] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    principal_details: Optional[PrincipalDetailsBase] = None
    hod_details: Optional[HODDetailsBase] = None
    faculty_details: Optional[FacultyDetailsBase] = None
    lab_assistant_details: Optional[LabAssistantDetailsBase] = None
    student_details: Optional[StudentDetailsBase] = None
    dte_admin_details: Optional[DTEAdminDetailsBase] = None
    admin_details: Optional[AdminDetailsBase] = None
