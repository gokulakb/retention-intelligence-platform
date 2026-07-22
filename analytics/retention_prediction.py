"""
Retention prediction using Machine Learning models.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from database.queries import get_users
import logging
import joblib
from config.config import MODELS_DIR

logger = logging.getLogger(__name__)

def prepare_data(session: Session, user_type: str = None):
    """Prepare feature matrix X and target y for modeling."""
    users_df = get_users(session, user_type=user_type)
    if users_df.empty:
        return None, None, None

    feature_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    # Ensure numeric
    for col in feature_cols:
        users_df[col] = pd.to_numeric(users_df[col], errors='coerce')

    # Drop rows with missing features
    users_df = users_df.dropna(subset=feature_cols)
    if len(users_df) < 10:
        return None, None, None

    # Target: retained if days_active > 30
    users_df['retained'] = (users_df['days_active'] > 30).astype(int)

    X = users_df[feature_cols]
    y = users_df['retained']
    return X, y, feature_cols

def train_models(session: Session, user_type: str = None):
    """
    Train Logistic Regression, Decision Tree, and Random Forest.
    Returns a dict of evaluation metrics, trained models, and feature names.
    """
    X, y, feature_cols = prepare_data(session, user_type)
    if X is None:
        return None, None, None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = {}
    trained_models = {}

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]

        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_proba)
        }
        trained_models[name] = model

    # Save artifacts
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, MODELS_DIR / 'scaler.pkl')
    for name, model in trained_models.items():
        joblib.dump(model, MODELS_DIR / f'{name}.pkl')

    # Save feature importance from RandomForest
    if 'RandomForest' in trained_models:
        importance = trained_models['RandomForest'].feature_importances_
        imp_df = pd.DataFrame({'feature': feature_cols, 'importance': importance})
        imp_df.to_csv(MODELS_DIR / 'feature_importance.csv', index=False)

    return results, trained_models, feature_cols

def predict_retention(session: Session, user_id: str):
    """
    Predict retention probability for a given user using the trained RandomForest.
    Returns probability (0-1).
    """
    try:
        model = joblib.load(MODELS_DIR / 'RandomForest.pkl')
        scaler = joblib.load(MODELS_DIR / 'scaler.pkl')
    except FileNotFoundError:
        logger.error("Model files not found. Train models first.")
        return None

    users_df = get_users(session, user_id=user_id)
    if users_df.empty:
        return None

    feature_cols = [
        'profile_completion', 'total_sessions', 'applications_submitted',
        'searches_performed', 'messages_sent', 'saved_opportunities',
        'session_duration_avg', 'days_active', 'time_to_first_action'
    ]
    for col in feature_cols:
        users_df[col] = pd.to_numeric(users_df[col], errors='coerce')

    X = users_df[feature_cols].fillna(0)
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[:, 1]
    return proba[0]