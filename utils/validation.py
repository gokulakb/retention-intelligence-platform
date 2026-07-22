"""
Data validation and completeness checks.
"""
import pandas as pd
from sqlalchemy.orm import Session
from database.queries import get_users
import logging

logger = logging.getLogger(__name__)

def check_missing_values(session: Session) -> dict:
    """Return a dict of column names -> count of missing values in the users table."""
    users_df = get_users(session)
    if users_df.empty:
        return {}
    missing = users_df.isnull().sum().to_dict()
    return missing

def check_duplicates(session: Session) -> int:
    """Return the number of duplicate user_id values."""
    users_df = get_users(session)
    if users_df.empty:
        return 0
    return users_df['user_id'].duplicated().sum()

def data_completeness(session: Session) -> dict:
    """
    Generate a comprehensive completeness report.
    Returns a dict with total users, duplicate count, and missing values per column.
    """
    total = len(get_users(session))
    duplicates = check_duplicates(session)
    missing = check_missing_values(session)
    return {
        "total_users": total,
        "duplicate_user_ids": duplicates,
        "missing_values": missing
    }

def reconcile_sources(session: Session) -> dict:
    """
    Compare counts between users and events to check for consistency.
    Returns dict with counts and discrepancy.
    """
    from database.queries import get_user_events
    users_df = get_users(session)
    events_df = get_user_events(session)

    user_count = len(users_df)
    event_user_count = len(events_df['user_id'].unique()) if not events_df.empty else 0

    return {
        "users_in_users_table": user_count,
        "users_with_events": event_user_count,
        "discrepancy": user_count - event_user_count
    }