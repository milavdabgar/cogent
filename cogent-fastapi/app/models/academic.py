from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class AcademicDepartment(Base):
    __tablename__ = "academic_departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)

    # Relationships
    degree_programs = relationship("DegreeProgram", back_populates="academic_department")

class DegreeLevel(Base):
    __tablename__ = "degree_levels"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    duration_years = Column(Float)
    status = Column(Boolean, default=True)

    # Relationships
    degree_programs = relationship("DegreeProgram", back_populates="degree_level")

class DegreeProgram(Base):
    __tablename__ = "degree_programs"

    id = Column(Integer, primary_key=True, index=True)
    academic_department_id = Column(Integer, ForeignKey("academic_departments.id"))
    degree_level_id = Column(Integer, ForeignKey("degree_levels.id"))
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    short_name = Column(String)
    total_credits_required = Column(Integer)
    status = Column(Boolean, default=True)

    # Relationships
    academic_department = relationship("AcademicDepartment", back_populates="degree_programs")
    degree_level = relationship("DegreeLevel", back_populates="degree_programs")
    program_subjects = relationship("ProgramSubject", back_populates="program")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    category = Column(String)  # Basic Science, Professional Core, etc.
    credits = Column(Integer)
    lecture_hours = Column(Integer)
    tutorial_hours = Column(Integer)
    practical_hours = Column(Integer)
    theory_exam_duration = Column(Float, nullable=True)
    practical_exam_duration = Column(Float, nullable=True)
    is_theory = Column(Boolean, default=True)
    is_practical = Column(Boolean, default=False)
    is_elective = Column(Boolean, default=False)
    max_theory_marks = Column(Integer, nullable=True)
    max_practical_marks = Column(Integer, nullable=True)
    passing_marks = Column(Integer)
    is_semipractical = Column(Boolean, default=False)
    is_functional = Column(Boolean, default=False)
    status = Column(Boolean, default=True)

    # Relationships
    program_subjects = relationship("ProgramSubject", back_populates="subject")

class ProgramSubject(Base):
    __tablename__ = "program_subjects"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("degree_programs.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    semester = Column(Integer)
    academic_year = Column(Integer)
    is_mandatory = Column(Boolean, default=True)

    # Relationships
    program = relationship("DegreeProgram", back_populates="program_subjects")
    subject = relationship("Subject", back_populates="program_subjects")
