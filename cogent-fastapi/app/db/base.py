from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import all models here for Alembic to detect them

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
