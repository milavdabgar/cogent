from datetime import date
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import SessionLocal
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate, GTUAdminDetailsBase
from app.models.user import UserRole, User
from sqlalchemy.orm import Session

def recreate_gtu_admin():
    db = SessionLocal()
    try:
        # Delete existing user
        existing_user = db.query(User).filter(User.email == "gtu.admin@gtu.ac.in").first()
        if existing_user:
            print(f"Deleting existing user with ID: {existing_user.id}")
            db.delete(existing_user)
            db.commit()
        
        # Create new user data
        user_in = UserCreate(
            email="gtu.admin@gtu.ac.in",
            password="gtuadmin123",  # This will be hashed by the create function
            first_name="GTU",
            last_name="Admin",
            phone_number="1234567890",
            date_of_birth=date(1990, 1, 1),
            role=UserRole.GTU_ADMIN,
            gtu_admin_details=GTUAdminDetailsBase(
                jurisdiction="Gujarat",
                date_of_joining=date(2024, 1, 1),
                access_level="full_access"
            )
        )
        
        # Create the new user
        user = crud_user.create(db, obj_in=user_in)
        print(f"GTU Admin recreated successfully with ID: {user.id}")
        
    except Exception as e:
        print(f"Error recreating GTU admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    recreate_gtu_admin()
