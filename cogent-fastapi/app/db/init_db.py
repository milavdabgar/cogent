from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import (
    User, UserRole, StudentDetails, FacultyDetails,
    HODDetails, PrincipalDetails, LabAssistantDetails
)
from datetime import date

def init_db(db: Session) -> None:
    # Create test users
    test_users = [
        {
            "email": "principal@cogent.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Principal",
            "role": UserRole.PRINCIPAL,
            "phone_number": "1234567890",
            "date_of_birth": date(1970, 1, 1),
            "is_active": True,
            "details": {
                "date_of_joining": date(2010, 1, 1),
                "qualification": "Ph.D. in Education Management",
                "experience_years": 20
            }
        },
        {
            "email": "hod@cogent.com",
            "password": "password123",
            "first_name": "Sarah",
            "last_name": "HOD",
            "role": UserRole.HOD,
            "phone_number": "2345678901",
            "date_of_birth": date(1975, 1, 1),
            "is_active": True,
            "details": {
                "department": "Computer Science",
                "date_of_joining": date(2012, 1, 1),
                "qualification": "Ph.D. in Computer Science",
                "experience_years": 15
            }
        },
        {
            "email": "faculty@cogent.com",
            "password": "password123",
            "first_name": "Michael",
            "last_name": "Faculty",
            "role": UserRole.FACULTY,
            "phone_number": "3456789012",
            "date_of_birth": date(1980, 1, 1),
            "is_active": True,
            "details": {
                "department": "Computer Science",
                "date_of_joining": date(2015, 1, 1),
                "qualification": "Ph.D. in Machine Learning",
                "specialization": "Artificial Intelligence"
            }
        },
        {
            "email": "lab@cogent.com",
            "password": "password123",
            "first_name": "David",
            "last_name": "Lab",
            "role": UserRole.LAB_ASSISTANT,
            "phone_number": "4567890123",
            "date_of_birth": date(1985, 1, 1),
            "is_active": True,
            "details": {
                "department": "Computer Science",
                "date_of_joining": date(2018, 1, 1),
                "lab_type": "Computer Networks Lab"
            }
        },
        {
            "email": "student@cogent.com",
            "password": "password123",
            "first_name": "Emily",
            "last_name": "Student",
            "role": UserRole.STUDENT,
            "phone_number": "5678901234",
            "date_of_birth": date(2000, 1, 1),
            "is_active": True,
            "details": {
                "enrollment_number": "CS2023001",
                "department": "Computer Science",
                "date_of_admission": date(2023, 1, 1),
                "current_semester": 2
            }
        }
    ]

    for user_data in test_users:
        # Check if user already exists
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            # Create new user
            hashed_password = get_password_hash(user_data["password"])
            user = User(
                email=user_data["email"],
                hashed_password=hashed_password,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=user_data["role"],
                phone_number=user_data["phone_number"],
                date_of_birth=user_data["date_of_birth"],
                is_active=user_data["is_active"]
            )
            db.add(user)
            db.flush()  # Flush to get the user ID

            # Add role-specific details
            if user.role == UserRole.PRINCIPAL:
                details = PrincipalDetails(
                    user_id=user.id,
                    date_of_joining=user_data["details"]["date_of_joining"],
                    qualification=user_data["details"]["qualification"],
                    experience_years=user_data["details"]["experience_years"]
                )
                db.add(details)
            
            elif user.role == UserRole.HOD:
                details = HODDetails(
                    user_id=user.id,
                    department=user_data["details"]["department"],
                    date_of_joining=user_data["details"]["date_of_joining"],
                    qualification=user_data["details"]["qualification"],
                    experience_years=user_data["details"]["experience_years"]
                )
                db.add(details)
            
            elif user.role == UserRole.FACULTY:
                details = FacultyDetails(
                    user_id=user.id,
                    department=user_data["details"]["department"],
                    date_of_joining=user_data["details"]["date_of_joining"],
                    qualification=user_data["details"]["qualification"],
                    specialization=user_data["details"]["specialization"]
                )
                db.add(details)
            
            elif user.role == UserRole.LAB_ASSISTANT:
                details = LabAssistantDetails(
                    user_id=user.id,
                    department=user_data["details"]["department"],
                    date_of_joining=user_data["details"]["date_of_joining"],
                    lab_type=user_data["details"]["lab_type"]
                )
                db.add(details)
            
            elif user.role == UserRole.STUDENT:
                details = StudentDetails(
                    user_id=user.id,
                    enrollment_number=user_data["details"]["enrollment_number"],
                    department=user_data["details"]["department"],
                    date_of_admission=user_data["details"]["date_of_admission"],
                    current_semester=user_data["details"]["current_semester"]
                )
                db.add(details)

    db.commit()
