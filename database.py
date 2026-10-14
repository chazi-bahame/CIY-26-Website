
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ciy.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )

if DATABASE_URL.startswith("postgresql://"):
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
