from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User, UserRole, StudentDetails
from datetime import date

def init_db(db: Session) -> None:
    # Create test users
    test_users = [
        {
            "email": "student@cogent.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Student",
            "role": UserRole.STUDENT,
            "phone_number": "1234567890",
            "date_of_birth": date(2000, 1, 1),
            "is_active": True
        },
        {
            "email": "faculty@cogent.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Faculty",
            "role": UserRole.FACULTY,
            "phone_number": "1234567890",
            "date_of_birth": date(1980, 1, 1),
            "is_active": True
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
            db.flush()

            # Add role-specific details
            if user.role == UserRole.STUDENT:
                student_details = StudentDetails(
                    user_id=user.id,
                    enrollment_number="TEST123",
                    department="Computer Science",
                    date_of_admission=date(2023, 1, 1),
                    current_semester=1
                )
                db.add(student_details)

    db.commit()
