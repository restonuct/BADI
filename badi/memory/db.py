"""
Database models for B.A.D.I. memory system

Uses SQLAlchemy for ORM and SQLite for storage.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

from badi.config import get_config

Base = declarative_base()


class User(Base):
    """User model for storing user profiles"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    preferences = relationship("Preference", back_populates="user", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"


class Preference(Base):
    """User preferences and settings"""
    __tablename__ = "preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<Preference(user_id={self.user_id}, key='{self.key}')>"


class Interaction(Base):
    """Conversation history and interactions"""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    # Column name is "metadata" in the database, but the attribute name
    # must not be "metadata" because SQLAlchemy reserves that attribute
    # for the Declarative Base metadata.
    interaction_metadata = Column("metadata", JSON, nullable=True)  # Store additional context
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    task = relationship("Task", back_populates="interactions")
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, role='{self.role}', user_id={self.user_id})>"


class Task(Base):
    """Task execution history and results"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)  # 'pending', 'running', 'completed', 'failed', 'cancelled'
    plan_json = Column(JSON, nullable=True)  # The generated plan
    result_json = Column(JSON, nullable=True)  # Execution results
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    interactions = relationship("Interaction", back_populates="task")
    
    def __repr__(self):
        return f"<Task(id={self.id}, goal='{self.goal[:50]}...', status='{self.status}')>"


class Memory(Base):
    """Long-term memory entries (for non-vector semantic memory)"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)
    importance = Column(Integer, default=5)  # 1-10 scale
    created_at = Column(DateTime, default=datetime.utcnow)
    accessed_at = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Memory(id={self.id}, category='{self.category}', importance={self.importance})>"


# Database engine and session factory
_engine = None
_SessionLocal = None


def get_engine():
    """Get or create database engine"""
    global _engine
    if _engine is None:
        config = get_config()
        database_url = f"sqlite:///{config.db_path}"
        _engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            echo=config.log_level == "DEBUG"
        )
    return _engine


def get_session_factory():
    """Get or create session factory"""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


def get_db() -> Session:
    """Get a database session"""
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, let caller manage


def init_db():
    """Initialize database tables"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


def get_or_create_user(db: Session, name: str = "Default User", email: Optional[str] = None) -> User:
    """Get or create a user"""
    # Try to find existing user
    user = db.query(User).filter(
        (User.name == name) | (User.email == email if email else False)
    ).first()
    
    if not user:
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user


def save_interaction(
    db: Session,
    user_id: int,
    role: str,
    content: str,
    task_id: Optional[int] = None,
    metadata: Optional[dict] = None
) -> Interaction:
    """Save an interaction to the database"""
    interaction = Interaction(
        user_id=user_id,
        role=role,
        content=content,
        task_id=task_id,
        interaction_metadata=metadata
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def save_task(
    db: Session,
    user_id: int,
    goal: str,
    status: str = "pending",
    plan_json: Optional[dict] = None
) -> Task:
    """Create a new task"""
    task = Task(
        user_id=user_id,
        goal=goal,
        status=status,
        plan_json=plan_json
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task_status(
    db: Session,
    task_id: int,
    status: str,
    result_json: Optional[dict] = None,
    error_message: Optional[str] = None
) -> Task:
    """Update task status and results"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        if result_json:
            task.result_json = result_json
        if error_message:
            task.error_message = error_message
        
        if status == "running" and not task.started_at:
            task.started_at = datetime.utcnow()
        elif status in ["completed", "failed", "cancelled"]:
            task.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(task)
    return task


def get_recent_interactions(
    db: Session,
    user_id: int,
    limit: int = 10,
    task_id: Optional[int] = None
) -> list[Interaction]:
    """Get recent interactions for context"""
    query = db.query(Interaction).filter(Interaction.user_id == user_id)
    
    if task_id:
        query = query.filter(Interaction.task_id == task_id)
    
    return query.order_by(Interaction.timestamp.desc()).limit(limit).all()


def save_preference(db: Session, user_id: int, key: str, value: str) -> Preference:
    """Save or update a user preference"""
    pref = db.query(Preference).filter(
        Preference.user_id == user_id,
        Preference.key == key
    ).first()
    
    if pref:
        pref.value = value
        pref.updated_at = datetime.utcnow()
    else:
        pref = Preference(user_id=user_id, key=key, value=value)
        db.add(pref)
    
    db.commit()
    db.refresh(pref)
    return pref


def get_preference(db: Session, user_id: int, key: str) -> Optional[str]:
    """Get a user preference value"""
    pref = db.query(Preference).filter(
        Preference.user_id == user_id,
        Preference.key == key
    ).first()
    return pref.value if pref else None
