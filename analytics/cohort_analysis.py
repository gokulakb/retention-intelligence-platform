"""
Cohort analysis functions with caching for performance.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.queries import get_users, get_user_events
from config.settings import COHORT_PERIODS
import streamlit as st
import logging

logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# Cached cohort functions
# ------------------------------------------------------------

@st.cache_data(ttl=3600)   # cache results for 1 hour
def build_cohorts(_session: Session, period: str = "weekly", user_type: str = None):
    """
    Build cohort table: users grouped by signup period, with retention per period.
    Returns a DataFrame with columns:
        cohort_period, cohort_type, user_type, period_number,
        retained_users, total_users_in_cohort, retention_rate
    """
    # Get users
    users_df = get_users(_session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    # Ensure datetime
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    users_df['last_active'] = pd.to_datetime(users_df['last_active'])

    # Determine cohort period
    if period == "weekly":
        users_df['cohort'] = users_df['created_at'].dt.strftime('%Y-W%W')
        # week number since cohort start
        users_df['cohort_start'] = users_df['created_at'] - pd.to_timedelta(users_df['created_at'].dt.weekday, unit='d')
        users_df['cohort_start'] = users_df['cohort_start'].dt.normalize()
    else:  # monthly
        users_df['cohort'] = users_df['created_at'].dt.strftime('%Y-%m')
        users_df['cohort_start'] = users_df['created_at'].dt.to_period('M').dt.start_time

    # For each user, compute periods active since signup
    max_periods = 52 if period == "weekly" else 24
    periods = range(max_periods + 1)

    # Get all users with their cohort
    cohorts = users_df.groupby('cohort').size().reset_index(name='total_users')

    # For each cohort, compute retention for each period
    results = []
    for cohort, group in users_df.groupby('cohort'):
        cohort_start = group['cohort_start'].iloc[0]
        total_users = len(group)
        for p in periods:
            if period == "weekly":
                period_end = cohort_start + timedelta(weeks=p+1)
                active = group[group['last_active'] >= period_end].shape[0]
            else:
                period_end = cohort_start + timedelta(days=30*(p+1))
                active = group[group['last_active'] >= period_end].shape[0]
            retention_rate = active / total_users if total_users > 0 else 0
            results.append({
                'cohort_period': cohort,
                'cohort_type': period,
                'user_type': user_type if user_type else 'all',
                'period_number': p,
                'retained_users': active,
                'total_users_in_cohort': total_users,
                'retention_rate': retention_rate
            })

    return pd.DataFrame(results)

@st.cache_data(ttl=3600)
def get_cohort_matrix(_session: Session, period: str = "weekly", user_type: str = None):
    """
    Return a pivot table for heatmap: rows=cohort, columns=period, values=retention_rate.
    """
    df = build_cohorts(_session, period, user_type)
    if df.empty:
        return pd.DataFrame()
    pivot = df.pivot(index='cohort_period', columns='period_number', values='retention_rate')
    # Sort cohorts by date
    pivot = pivot.sort_index()
    return pivot

# ------------------------------------------------------------
# Non‑cached helpers (if needed)
# ------------------------------------------------------------

def get_cohort_summary(_session: Session, period: str = "weekly", user_type: str = None):
    """
    Return a summary of cohorts (e.g., total users per cohort) without caching.
    Used for live counts.
    """
    users_df = get_users(_session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    if period == "weekly":
        users_df['cohort'] = users_df['created_at'].dt.strftime('%Y-W%W')
    else:
        users_df['cohort'] = users_df['created_at'].dt.strftime('%Y-%m')
    summary = users_df.groupby('cohort').size().reset_index(name='users')
    return summary