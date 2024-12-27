from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    departments = relationship("Department", back_populates="college")

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    hod_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    college = relationship("College", back_populates="departments")
    hod = relationship("User", foreign_keys=[hod_id])
