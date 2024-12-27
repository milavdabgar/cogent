from .crud_user import user
from .crud_college import college, department as college_department
from .crud_academic import (
    department,
    degree_level,
    degree_program,
    subject,
    program_subject
)

__all__ = [
    "user",
    "college",
    "college_department",
    "department",
    "degree_level",
    "degree_program",
    "subject",
    "program_subject"
]
