"""
User segmentation using K-Means clustering on behavioral features.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from database.queries import get_users
import logging

logger = logging.getLogger(__name__)

def segment_users(session: Session, user_type: str = None, n_clusters: int = 4):
    """
    Perform K-Means clustering on behavioral features.
    Returns DataFrame with cluster labels.
    """
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return pd.DataFrame()

    feature_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    # Ensure numeric
    for col in feature_cols:
        users_df[col] = pd.to_numeric(users_df[col], errors='coerce')

    # Drop rows with missing features
    users_df_clean = users_df.dropna(subset=feature_cols)
    if len(users_df_clean) < n_clusters:
        logger.warning("Not enough data for clustering.")
        return pd.DataFrame()

    X = users_df_clean[feature_cols]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    users_df_clean['cluster'] = clusters
    return users_df_clean[['user_id', 'user_type', 'cluster'] + feature_cols]