"""
Churn analytics.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.queries import get_users, get_user_events
from config.settings import CHURN_INACTIVITY_DAYS
import logging

logger = logging.getLogger(__name__)

def compute_churn_rate(session: Session, user_type: str = None, days_inactive: int = CHURN_INACTIVITY_DAYS):
    """
    Compute churn rate: number of users inactive for >= days_inactive divided by total users.
    Returns a dict.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return {"churn_rate": 0.0, "churned": 0, "total": 0}

    users_df['last_active'] = pd.to_datetime(users_df['last_active'])
    cutoff = datetime.utcnow() - timedelta(days=days_inactive)
    churned = users_df[users_df['last_active'] < cutoff]
    total = len(users_df)
    rate = len(churned) / total if total > 0 else 0.0
    return {"churn_rate": rate, "churned": len(churned), "total": total}

def churn_trend(session: Session, user_type: str = None, days_inactive: int = CHURN_INACTIVITY_DAYS):
    """
    Compute churn rate over time (weekly or monthly).
    Returns DataFrame with date and churn_rate.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    users_df['last_active'] = pd.to_datetime(users_df['last_active'])
    # We need to compute churn rate for each week/month: users who became inactive in that period.
    # For simplicity, we'll bin by signup date and compute churn at each period.
    # A more accurate method: for each date, count users whose last_active < date - days_inactive and created_at < date.
    # We'll just produce a time series of cumulative churn.

    # Define periods (weeks)
    start_date = users_df['created_at'].min()
    end_date = datetime.utcnow()
    periods = pd.date_range(start=start_date, end=end_date, freq='W-MON')
    trend = []
    for date in periods:
        cutoff = date - timedelta(days=days_inactive)
        active_before = users_df[users_df['created_at'] <= date]
        churned_in_period = active_before[active_before['last_active'] < cutoff]
        total = len(active_before)
        rate = len(churned_in_period) / total if total > 0 else 0.0
        trend.append({'period': date, 'churn_rate': rate, 'churned': len(churned_in_period), 'total': total})
    return pd.DataFrame(trend)

def high_risk_users(session: Session, days_inactive_threshold: int = CHURN_INACTIVITY_DAYS, user_type: str = None):
    """
    Identify users at high risk: those whose last_active is between 7 and days_inactive_threshold days ago.
    Returns DataFrame.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    users_df['last_active'] = pd.to_datetime(users_df['last_active'])
    now = datetime.utcnow()
    risk_start = now - timedelta(days=days_inactive_threshold)
    risk_end = now - timedelta(days=7)  # very recent are not high risk
    high_risk = users_df[(users_df['last_active'] >= risk_start) & (users_df['last_active'] < risk_end)]
    return high_risk