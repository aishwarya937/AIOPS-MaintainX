from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Connection URL (User: admin, Pass: password123, DB: maintainx)
DATABASE_URL = "postgresql://admin:password123@127.0.0.1:5433/maintainx"

# 2. Create the Engine (The Bridge)
engine = create_engine(DATABASE_URL)

# 3. Create the Session (The Conversation)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base Model (The Template)
Base = declarative_base()

# 5. Dependency (Used later by API to get access)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()