from typing import Optional, List
from pydantic import BaseModel, EmailStr

class CollegeBase(BaseModel):
    name: str
    code: str
    address: str
    city: str
    state: str
    country: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    is_active: bool = True

class CollegeCreate(CollegeBase):
    pass

class CollegeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None

class DepartmentBase(BaseModel):
    name: str
    code: str
    college_id: int
    hod_id: Optional[int] = None
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    hod_id: Optional[int] = None
    is_active: Optional[bool] = None

class Department(DepartmentBase):
    id: int
    
    class Config:
        orm_mode = True

class College(CollegeBase):
    id: int
    departments: List[Department] = []
    
    class Config:
        orm_mode = True
