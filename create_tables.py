from app.db.session import engine
from app.db.base import Base
from app.models import user, console, buffet

# ساخت جدول‌ها
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
