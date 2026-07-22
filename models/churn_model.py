"""
Churn prediction model.
"""
from analytics.churn_analysis import high_risk_users, compute_churn_rate
import pandas as pd

def get_churn_risk_users(session, user_type=None, days=30):
    """Return high-risk users."""
    return high_risk_users(session, days_inactive_threshold=days, user_type=user_type)