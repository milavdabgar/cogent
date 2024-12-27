import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User, UserRole, AdminDetails
from app.core.security import get_password_hash

def create_superadmin(email: str, password: str, first_name: str, last_name: str):
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == email).first()
        if existing_admin:
            print(f"User with email {email} already exists")
            return

        # Create admin user
        admin = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN,
            is_active=True,
            last_login=datetime.now().date()
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        # Create admin details
        admin_details = AdminDetails(
            user_id=admin.id,
            super_admin=True,
            date_of_joining=datetime.now().date(),
            access_level="full"
        )
        db.add(admin_details)
        db.commit()

        print(f"Successfully created superadmin user: {email}")

    except Exception as e:
        print(f"Error creating superadmin: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python create_superadmin.py <email> <password> <first_name> <last_name>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    first_name = sys.argv[3]
    last_name = sys.argv[4]
    
    create_superadmin(email, password, first_name, last_name)
