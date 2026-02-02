from app.models import user, console, buffet,unitPrice
from app.db.session import engine
from app.db.base import Base

# ساخت جدول‌ها
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
