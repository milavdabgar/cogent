from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData
)
from app.schemas.profile import (
    ProfileUpdate,
    ProfileResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)
from app.schemas.college import (
    CollegeCreate,
    CollegeUpdate,
    CollegeResponse,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    FacultyCourseAssignmentCreate,
    FacultyCourseAssignmentUpdate,
    FacultyCourseAssignmentResponse
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "ProfileUpdate",
    "ProfileResponse",
    "PasswordChange",
    "PasswordReset",
    "PasswordResetConfirm",
    "CollegeCreate",
    "CollegeUpdate",
    "CollegeResponse",
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "FacultyCourseAssignmentCreate",
    "FacultyCourseAssignmentUpdate",
    "FacultyCourseAssignmentResponse"
]
