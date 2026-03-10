import os
import uuid
from datetime import datetime
from sqlalchemy import (Column, String, DateTime, Boolean, ForeignKey,
                        create_engine, func)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ---------------------------------------------------------------------------
# Database URL handling with prefix fixing and SSL configuration
# ---------------------------------------------------------------------------
raw_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite:///./app.db"
if raw_url.startswith("postgresql+asyncpg://"):
    raw_url = raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg://")

# Determine if we need SSL connect args (non‑localhost and non‑sqlite)
if raw_url.startswith("sqlite"):
    engine = create_engine(raw_url, connect_args={"check_same_thread": False})
else:
    # Add sslmode=require when not connecting to localhost
    connect_args = {}
    if "localhost" not in raw_url:
        connect_args["sslmode"] = "require"
    engine = create_engine(raw_url, connect_args=connect_args, pool_pre_ping=True)

# ---------------------------------------------------------------------------
# SQLAlchemy setup
# ---------------------------------------------------------------------------
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Prefix for all tables (prevents collisions in shared DB)
_TABLE_PREFIX = "tk_"

class TaskModel(Base):
    __tablename__ = f"{_TABLE_PREFIX}tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, nullable=True)  # low, medium, high
    category = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    subtasks = relationship("SubtaskModel", back_populates="task", cascade="all, delete-orphan")

class SubtaskModel(Base):
    __tablename__ = f"{_TABLE_PREFIX}subtasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey(f"{_TABLE_PREFIX}tasks.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    task = relationship("TaskModel", back_populates="subtasks")

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)
