"""
Executive KPI Dashboard.
"""
import streamlit as st
import pandas as pd
from database.database import SessionLocal
from utils.metrics import *
from utils.charts import plotly_bar_chart, plotly_line_chart
from datetime import datetime, timedelta
import plotly.express as px

def executive_dashboard():
    st.markdown('<div class="main-header">Executive KPI Dashboard</div>', unsafe_allow_html=True)

    session = SessionLocal()
    try:
        # Compute KPIs
        total_users = get_total_users(session)
        active_users = get_active_users(session)
        candidate_retention = get_retention_rate(session, user_type="candidate", window=4)
        company_retention = get_retention_rate(session, user_type="company", window=4)
        weekly_retention = get_retention_rate(session, period="weekly", window=1)
        monthly_retention = get_retention_rate(session, period="monthly", window=1)
        churn_rate = get_churn_rate(session)
        growth_rate = get_growth_rate(session)
        user_lifetime = get_user_lifetime(session)
        retention_score = get_retention_score(session)

        # Display KPI cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", f"{total_users:,}")
        with col2:
            st.metric("Active Users (30d)", f"{active_users:,}")
        with col3:
            st.metric("Candidate Retention (4w)", f"{candidate_retention:.1%}")
        with col4:
            st.metric("Company Retention (4w)", f"{company_retention:.1%}")

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("Weekly Retention", f"{weekly_retention:.1%}")
        with col6:
            st.metric("Monthly Retention", f"{monthly_retention:.1%}")
        with col7:
            st.metric("Churn Rate", f"{churn_rate:.1%}")
        with col8:
            st.metric("Growth Rate", f"{growth_rate:.1f}%")

        col9, col10 = st.columns(2)
        with col9:
            st.metric("User Lifetime (avg days)", f"{user_lifetime:.1f}")
        with col10:
            st.metric("Retention Score", f"{retention_score:.1%}")

        # Trends: churn trend
        st.subheader("Churn Trend Over Time")
        from analytics.churn_analysis import churn_trend
        trend_df = churn_trend(session)
        if not trend_df.empty:
            fig = px.line(trend_df, x='period', y='churn_rate', title="Weekly Churn Rate")
            st.plotly_chart(fig, use_container_width=True)

        # Retention by user type (bar chart)
        st.subheader("Retention by User Type")
        retention_data = {
            "User Type": ["Candidate", "Company"],
            "Retention (4w)": [candidate_retention, company_retention]
        }
        df_ret = pd.DataFrame(retention_data)
        fig = px.bar(df_ret, x="User Type", y="Retention (4w)", title="Retention by User Type")
        st.plotly_chart(fig, use_container_width=True)

    finally:
        session.close()