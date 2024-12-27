from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class UserRole(str, enum.Enum):
    DTE_ADMIN = "dte_admin"
    GTU_ADMIN = "gtu_admin"
    ADMIN = "admin"
    PRINCIPAL = "principal"
    HOD = "hod"
    FACULTY = "faculty"
    LAB_ASSISTANT = "lab_assistant"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    last_login = Column(Date, nullable=True)
    
    # Role specific details
    dte_admin_details = relationship("DTEAdminDetails", back_populates="user", uselist=False)
    admin_details = relationship("AdminDetails", back_populates="user", uselist=False)
    principal_details = relationship("PrincipalDetails", back_populates="user", uselist=False)
    hod_details = relationship("HODDetails", back_populates="user", uselist=False)
    faculty_details = relationship("FacultyDetails", back_populates="user", uselist=False)
    lab_assistant_details = relationship("LabAssistantDetails", back_populates="user", uselist=False)
    student_details = relationship("StudentDetails", back_populates="user", uselist=False)
    gtu_admin_details = relationship("GTUAdminDetails", back_populates="user", uselist=False)

class PrincipalDetails(Base):
    __tablename__ = "principal_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    date_of_joining = Column(Date)
    qualification = Column(String)
    experience_years = Column(Integer)
    
    user = relationship("User", back_populates="principal_details")

class HODDetails(Base):
    __tablename__ = "hod_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    department = Column(String)
    date_of_joining = Column(Date)
    qualification = Column(String)
    experience_years = Column(Integer)
    
    user = relationship("User", back_populates="hod_details")

class FacultyDetails(Base):
    __tablename__ = "faculty_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    department = Column(String)
    date_of_joining = Column(Date)
    qualification = Column(String)
    specialization = Column(String)
    
    user = relationship("User", back_populates="faculty_details")

class LabAssistantDetails(Base):
    __tablename__ = "lab_assistant_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    department = Column(String)
    date_of_joining = Column(Date)
    lab_type = Column(String)
    
    user = relationship("User", back_populates="lab_assistant_details")

class StudentDetails(Base):
    __tablename__ = "student_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    enrollment_number = Column(String, unique=True)
    department = Column(String)
    date_of_admission = Column(Date)
    current_semester = Column(Integer)
    
    user = relationship("User", back_populates="student_details")

class AdminDetails(Base):
    __tablename__ = "admin_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    super_admin = Column(Boolean, default=False)  # For distinguishing super admins
    date_of_joining = Column(Date)
    access_level = Column(String)  # Can be used to define different admin access levels
    
    user = relationship("User", back_populates="admin_details")

class DTEAdminDetails(Base):
    __tablename__ = "dte_admin_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    jurisdiction = Column(String)  # e.g., "Gujarat"
    date_of_joining = Column(Date)
    access_level = Column(String)
    
    user = relationship("User", back_populates="dte_admin_details")

class GTUAdminDetails(Base):
    __tablename__ = "gtu_admin_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    jurisdiction = Column(String)  # e.g., "Gujarat"
    date_of_joining = Column(Date)
    access_level = Column(String)
    
    user = relationship("User", back_populates="gtu_admin_details")
