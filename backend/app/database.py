from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file
DATABASE_URL = "sqlite:///job_tracker.db"

# Database engine used to communicate with SQLite
engine = create_engine(DATABASE_URL)

# Factory used to create new database sessions
SessionLocal = sessionmaker(bind=engine)

# Base class inherited by all database models
Base = declarative_base()