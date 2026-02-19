from app.models import user, console, buffet, unitPrice, bill, billFood
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
