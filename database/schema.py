"""
SQLAlchemy ORM models for the platform.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    user_type = Column(String)  # 'candidate' or 'company'
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime)
    profile_completion = Column(Float, default=0.0)
    total_sessions = Column(Integer, default=0)
    applications_submitted = Column(Integer, default=0)
    searches_performed = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    saved_opportunities = Column(Integer, default=0)
    session_duration_avg = Column(Float, default=0.0)
    days_active = Column(Integer, default=0)
    time_to_first_action = Column(Float, nullable=True)

    # Relationships
    company = relationship("Company", back_populates="users")   # <-- added
    events = relationship("Event", back_populates="user")
    applications = relationship("Application", back_populates="user")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    industry = Column(String)
    size = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="company")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_metadata = Column(Text, nullable=True)   # renamed from 'metadata'

    user = relationship("User", back_populates="events")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    job_title = Column(String)
    applied_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)

    user = relationship("User", back_populates="applications")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    activity_date = Column(Date)
    activity_count = Column(Integer, default=0)

class RetentionMetric(Base):
    __tablename__ = "retention"

    id = Column(Integer, primary_key=True, index=True)
    cohort_period = Column(String)
    cohort_type = Column(String)
    user_type = Column(String)
    period_number = Column(Integer)
    retained_users = Column(Integer)
    total_users_in_cohort = Column(Integer)
    retention_rate = Column(Float)