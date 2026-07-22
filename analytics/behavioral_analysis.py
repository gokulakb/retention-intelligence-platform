"""
Behavioral analysis: compute metrics, feature importance, correlations.
"""
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database.queries import get_users
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import logging

logger = logging.getLogger(__name__)

def compute_behavioral_features(session: Session, user_type: str = None):
    """Return a DataFrame of behavioral features for users."""
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    # Select relevant columns
    feature_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    # Ensure numeric
    for col in feature_cols:
        users_df[col] = pd.to_numeric(users_df[col], errors='coerce')

    # Drop rows with missing essential features
    users_df = users_df.dropna(subset=feature_cols)
    return users_df[feature_cols]

def behavioral_correlation_with_retention(session: Session, user_type: str = None):
    """
    Compute correlation of behavioral features with retention (days_active > 30 as proxy).
    Returns DataFrame with feature and correlation.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    users_df['retention_target'] = (users_df['days_active'] > 30).astype(int)

    feature_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    for col in feature_cols:
        users_df[col] = pd.to_numeric(users_df[col], errors='coerce')

    # Correlation with retention_target (boolean)
    corr = users_df[feature_cols + ['retention_target']].corr()['retention_target'].drop('retention_target')
    return corr.reset_index().rename(columns={'index': 'feature', 'retention_target': 'correlation'})

def feature_importance_for_retention(session: Session, user_type: str = None):
    """
    Use Random Forest to determine feature importance for predicting retention.
    Returns DataFrame with feature and importance.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    feature_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    for col in feature_cols:
        users_df[col] = pd.to_numeric(users_df[col], errors='coerce')

    users_df = users_df.dropna(subset=feature_cols)
    if len(users_df) < 10:
        return pd.DataFrame()

    users_df['retained'] = (users_df['days_active'] > 30).astype(int)

    X = users_df[feature_cols]
    y = users_df['retained']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_scaled, y)

    importance = rf.feature_importances_
    feature_importance = pd.DataFrame({'feature': feature_cols, 'importance': importance})
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    return feature_importance