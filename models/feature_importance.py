"""
Feature importance analysis.
"""
from analytics.behavioral_analysis import feature_importance_for_retention

def get_feature_importance(session, user_type=None):
    """Return feature importance DataFrame."""
    return feature_importance_for_retention(session, user_type)