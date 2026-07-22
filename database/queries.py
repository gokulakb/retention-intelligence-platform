"""
Common database queries with caching for production performance.
"""
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from database.schema import User, Event, Application, ActivityLog, RetentionMetric
from datetime import datetime, timedelta, date
import streamlit as st

# ------------------------------------------------------------
# Cached queries – results reused across sessions
# ------------------------------------------------------------

@st.cache_data(ttl=3600)   # cache for 1 hour
def get_users(_session: Session, user_type: str = None, active_only: bool = False):
    """
    Return users as DataFrame.
    The underscore in _session tells Streamlit not to hash the session object.
    """
    query = _session.query(User)
    if user_type:
        query = query.filter(User.user_type == user_type)
    if active_only:
        cutoff = datetime.utcnow() - timedelta(days=30)
        query = query.filter(User.last_active >= cutoff)
    df = pd.read_sql(query.statement, _session.bind)
    return df

@st.cache_data(ttl=3600)
def get_user_events(_session: Session, user_id: str = None, start_date=None, end_date=None):
    query = _session.query(Event)
    if user_id:
        query = query.filter(Event.user_id == user_id)
    if start_date:
        query = query.filter(Event.timestamp >= start_date)
    if end_date:
        query = query.filter(Event.timestamp <= end_date)
    df = pd.read_sql(query.statement, _session.bind)
    return df

@st.cache_data(ttl=3600)
def get_applications(_session: Session, user_id: str = None):
    query = _session.query(Application)
    if user_id:
        query = query.filter(Application.user_id == user_id)
    df = pd.read_sql(query.statement, _session.bind)
    return df

@st.cache_data(ttl=3600)
def get_retention_metrics(_session: Session, cohort_type: str = None, user_type: str = None):
    query = _session.query(RetentionMetric)
    if cohort_type:
        query = query.filter(RetentionMetric.cohort_type == cohort_type)
    if user_type:
        query = query.filter(RetentionMetric.user_type == user_type)
    df = pd.read_sql(query.statement, _session.bind)
    return df

# ------------------------------------------------------------
# Non‑cached helpers (live counts, etc.)
# ------------------------------------------------------------

def get_active_users_count(session: Session, days: int = 30):
    """Count users active within last `days` days (live query – not cached)."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    count = session.query(User).filter(User.last_active >= cutoff).count()
    return count

def get_churned_users(session: Session, days_inactive: int = 30, user_type: str = None):
    """Return users who have not been active for >= days_inactive (live query)."""
    cutoff = datetime.utcnow() - timedelta(days=days_inactive)
    query = session.query(User).filter(User.last_active < cutoff)
    if user_type:
        query = query.filter(User.user_type == user_type)
    df = pd.read_sql(query.statement, session.bind)
    return df