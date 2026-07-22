"""
Anomaly detection on key metrics using statistical methods (IQR, Z-score).
"""
import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from database.queries import get_users

def detect_outliers_iqr(df: pd.DataFrame, column: str, multiplier: float = 1.5):
    """Return rows where column values are outliers using IQR."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return df[(df[column] < lower) | (df[column] > upper)]

def detect_outliers_zscore(df: pd.DataFrame, column: str, threshold: float = 3):
    """Return rows where column values have Z-score > threshold."""
    z = np.abs(stats.zscore(df[column].dropna()))
    outliers = df.loc[z > threshold]
    return outliers

def get_anomaly_report(session: Session, user_type: str = None):
    """
    Generate an anomaly report for key behavioral metrics.
    Returns a dict with outliers for each metric.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return {}

    numeric_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    report = {}
    for col in numeric_cols:
        if col in users_df.columns:
            outliers = detect_outliers_iqr(users_df, col)
            if not outliers.empty:
                report[col] = outliers[['user_id', col]].to_dict(orient='records')
    return report