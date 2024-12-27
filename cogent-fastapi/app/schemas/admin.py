from typing import Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr

class AdminDetailsBase(BaseModel):
    super_admin: bool = False
    access_level: Optional[str] = None
    date_of_joining: Optional[date] = None

class AdminDetailsCreate(AdminDetailsBase):
    pass

class AdminDetailsUpdate(AdminDetailsBase):
    pass

class AdminDetails(AdminDetailsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Schemas for admin operations
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_active: Optional[bool] = None

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool
    last_login: Optional[date]

    class Config:
        orm_mode = True

class AdminStats(BaseModel):
    total_users: int
    active_students: int
    active_faculty: int

class SystemHealth(BaseModel):
    service_name: str
    status: str
    uptime: float
    last_check: date

class RecentActivity(BaseModel):
    id: int
    action: str
    description: str
    timestamp: date
    user_id: int
    user_email: str
