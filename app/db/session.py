from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# ساخت engine دیتابیس
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # مخصوص SQLite
)

# ساخت session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()