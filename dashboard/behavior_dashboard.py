"""
Behavioral Insights Dashboard page.
"""
import streamlit as st
import pandas as pd
from database.database import SessionLocal
from analytics.behavioral_analysis import (
    compute_behavioral_features,
    behavioral_correlation_with_retention,
    feature_importance_for_retention
)
import plotly.express as px

def behavior_dashboard():
    st.markdown('<div class="main-header">Behavioral Insights</div>', unsafe_allow_html=True)

    session = SessionLocal()
    try:
        user_type = st.selectbox("User Type", ["all", "candidate", "company"], index=0)
        if user_type == "all":
            user_type = None

        # Feature importance
        st.subheader("Feature Importance for Retention")
        imp_df = feature_importance_for_retention(session, user_type)
        if not imp_df.empty:
            fig = px.bar(imp_df, x='feature', y='importance',
                         title="Feature Importance (Random Forest)",
                         color='importance', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for feature importance.")

        # Correlation with retention
        st.subheader("Correlation with Retention")
        corr_df = behavioral_correlation_with_retention(session, user_type)
        if not corr_df.empty:
            fig = px.bar(corr_df, x='feature', y='correlation',
                         title="Correlation of Features with Retention",
                         color='correlation', color_continuous_scale='RdBu_r')
            st.plotly_chart(fig, use_container_width=True)

        # Distribution of a selected feature
        features_df = compute_behavioral_features(session, user_type)
        if not features_df.empty:
            st.subheader("Feature Distribution")
            selected = st.selectbox("Select a feature", features_df.columns)
            fig = px.histogram(features_df, x=selected,
                               title=f"Distribution of {selected}")
            st.plotly_chart(fig, use_container_width=True)

            # Correlation matrix
            st.subheader("Correlation Matrix")
            corr_matrix = features_df.corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                            color_continuous_scale="RdBu_r",
                            title="Behavioral Feature Correlation")
            st.plotly_chart(fig, use_container_width=True)

    finally:
        session.close()