from app.database import SessionLocal

# Creates a database session for a request and closes it afterward
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()