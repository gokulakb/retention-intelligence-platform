"""
Retention model interface.
"""
from analytics.retention_prediction import train_models, predict_retention

def train_retention_models(session, user_type=None):
    """Train models and return results."""
    return train_models(session, user_type)

def get_retention_probability(session, user_id):
    """Get retention probability for a user."""
    return predict_retention(session, user_id)