from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class CourseType(str, enum.Enum):
    THEORY = "theory"
    PRACTICAL = "practical"
    PROJECT = "project"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    credits = Column(Integer)
    type = Column(Enum(CourseType))
    semester = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    department = relationship("Department", back_populates="courses")
    faculty_assignments = relationship("FacultyCourseAssignment", back_populates="course")

class FacultyCourseAssignment(Base):
    __tablename__ = "faculty_course_assignments"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    academic_year = Column(String)  # e.g., "2023-24"
    semester = Column(Integer)  # 1 to 8
    is_active = Column(Boolean, default=True)
    
    # Relationships
    faculty = relationship("User")
    course = relationship("Course", back_populates="faculty_assignments")
