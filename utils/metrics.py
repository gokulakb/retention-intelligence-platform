"""
Core metric computations for KPIs.
"""
from sqlalchemy.orm import Session
from database.queries import get_users, get_active_users_count
from config.settings import CHURN_INACTIVITY_DAYS
import pandas as pd
from datetime import datetime, timedelta

def get_total_users(session: Session, user_type: str = None) -> int:
    """Total number of users, optionally filtered by user_type."""
    df = get_users(session, user_type=user_type)
    return len(df)

def get_active_users(session: Session, user_type: str = None, days: int = 30) -> int:
    """Count of users active within the last `days` days."""
    return get_active_users_count(session, days=days)

def get_retention_rate(session: Session, user_type: str = None,
                       period: str = "weekly", window: int = 4) -> float:
    """
    Average retention rate at a given period window (e.g., week 4, month 3).
    Uses cohort analysis data.
    """
    from analytics.cohort_analysis import build_cohorts
    cohorts = build_cohorts(session, period, user_type)
    if cohorts.empty:
        return 0.0
    df_window = cohorts[cohorts['period_number'] == window]
    if df_window.empty:
        return 0.0
    return df_window['retention_rate'].mean()

def get_churn_rate(session: Session, user_type: str = None,
                   days_inactive: int = CHURN_INACTIVITY_DAYS) -> float:
    """Overall churn rate based on inactivity threshold."""
    from analytics.churn_analysis import compute_churn_rate
    res = compute_churn_rate(session, user_type, days_inactive)
    return res['churn_rate']

def get_growth_rate(session: Session, user_type: str = None, days: int = 30) -> float:
    """
    Percentage growth in user count over the last `days` days compared
    to the previous `days` days.
    """
    now = datetime.utcnow()
    current_start = now - timedelta(days=days)
    previous_start = current_start - timedelta(days=days)

    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return 0.0
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])

    current = users_df[users_df['created_at'] >= current_start]
    previous = users_df[(users_df['created_at'] >= previous_start) &
                        (users_df['created_at'] < current_start)]

    current_count = len(current)
    previous_count = len(previous)
    if previous_count == 0:
        return 0.0
    return ((current_count - previous_count) / previous_count) * 100

def get_user_lifetime(session: Session, user_type: str = None) -> float:
    """
    Average lifetime (in days) for users who have churned
    (inactive for at least 30 days).
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return 0.0
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    users_df['last_active'] = pd.to_datetime(users_df['last_active'])

    cutoff = datetime.utcnow() - timedelta(days=30)
    churned = users_df[users_df['last_active'] < cutoff]
    if churned.empty:
        return 0.0
    lifetime = (churned['last_active'] - churned['created_at']).dt.days
    return lifetime.mean()

def get_retention_score(session: Session, user_type: str = None) -> float:
    """
    Composite retention score – weighted average of weekly (4‑week) and
    monthly (3‑month) retention.
    """
    weekly = get_retention_rate(session, user_type, "weekly", 4)
    monthly = get_retention_rate(session, user_type, "monthly", 3)
    return (weekly + monthly) / 2