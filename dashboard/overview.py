"""
Home page / Overview.
"""
import streamlit as st
import pandas as pd
from database.database import SessionLocal
from utils.metrics import *
from utils.validation import data_completeness
import plotly.express as px

def overview_page():
    st.markdown('<div class="main-header">Retention Intelligence & Cohort Analytics Platform</div>', unsafe_allow_html=True)
    st.markdown("Welcome to the enterprise-grade retention analytics solution.")

    # Quick metrics
    session = SessionLocal()
    try:
        total_users = get_total_users(session)
        active_users = get_active_users(session)
        churn_rate = get_churn_rate(session)
        retention_score = get_retention_score(session)
        growth = get_growth_rate(session)
    finally:
        session.close()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", f"{total_users:,}")
    with col2:
        st.metric("Active Users (30d)", f"{active_users:,}")
    with col3:
        st.metric("Churn Rate", f"{churn_rate:.1%}")
    with col4:
        st.metric("Retention Score", f"{retention_score:.1%}", delta=f"{growth:.1f}%")

    # Data validation summary
    st.subheader("Data Validation Summary")
    session = SessionLocal()
    try:
        completeness = data_completeness(session)
        st.write(f"Total Users: {completeness['total_users']}")
        st.write(f"Duplicate User IDs: {completeness['duplicate_user_ids']}")
        st.write("Missing values per column:")
        st.json(completeness['missing_values'])
    finally:
        session.close()

    st.markdown("### Quick Actions")
    st.info("Use the sidebar to navigate to detailed dashboards for Cohort, Churn, Behavioral, and Predictive Analytics.")