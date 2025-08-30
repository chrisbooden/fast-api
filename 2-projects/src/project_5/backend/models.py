from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime, Enum
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class Logs(Base):
    __tablename__ = 'tbl_logs'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    request_type = Column(String, nullable=False)
    query_params = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime(timezone=True), nullable=True)
    run_time = Column(Integer, nullable=True)
    completed = Column(Boolean, nullable=False)
    msg = Column(String(1000), nullable=True)

class Users(Base):
    __tablename__ = 'tbl_users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(Integer, ForeignKey("tbl_logs.log_id"))
    user_name = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String, nullable=False)

class Todos(Base):
    __tablename__ = 'tbl_todos'

    todo_id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(Integer, ForeignKey("tbl_logs.log_id"))
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    completed = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id"), nullable=False)