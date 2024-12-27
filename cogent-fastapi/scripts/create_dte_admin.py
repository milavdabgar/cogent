import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services import user as user_service
from app.schemas.user import UserCreate, DTEAdminDetailsBase

def create_dte_admin():
    db = SessionLocal()
    try:
        # Create DTE admin user
        user_data = UserCreate(
            email="dte.admin@cogent.edu",
            password="Cogent@123",
            first_name="DTE",
            last_name="Admin",
            phone_number="9876543210",
            date_of_birth=date(1980, 1, 1),
            role="dte_admin",
            dte_admin_details=DTEAdminDetailsBase(
                jurisdiction="Maharashtra",
                date_of_joining=date(2024, 1, 1),
                access_level="full"
            )
        )
        
        user = user_service.create_user(db, user_data)
        print(f"Created DTE admin user with ID: {user.id}")
        
    except Exception as e:
        print(f"Error creating DTE admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_dte_admin()
