"""
Cohort Analysis Dashboard page.
"""
import streamlit as st
import pandas as pd
from database.database import SessionLocal
from analytics.cohort_analysis import build_cohorts, get_cohort_matrix
from utils.charts import plotly_heatmap
import plotly.express as px

def cohort_dashboard():
    st.markdown('<div class="main-header">Cohort Analysis</div>', unsafe_allow_html=True)

    session = SessionLocal()
    try:
        col1, col2 = st.columns(2)
        with col1:
            period = st.selectbox("Cohort Period", ["weekly", "monthly"], index=0)
        with col2:
            user_type = st.selectbox("User Type", ["all", "candidate", "company"], index=0)
            if user_type == "all":
                user_type = None

        cohorts_df = build_cohorts(session, period=period, user_type=user_type)
        if cohorts_df.empty:
            st.warning("No data for the selected filters.")
            return

        # Heatmap
        st.subheader("Retention Matrix Heatmap")
        pivot = get_cohort_matrix(session, period=period, user_type=user_type)
        if not pivot.empty:
            fig = plotly_heatmap(pivot, title="Retention Rate by Cohort",
                                 xlabel="Period Number", ylabel="Cohort")
            st.plotly_chart(fig, use_container_width=True)

        # Retention curves
        st.subheader("Retention Curves")
        fig = px.line(cohorts_df, x="period_number", y="retention_rate",
                      color="cohort_period", title="Retention Curves by Cohort")
        st.plotly_chart(fig, use_container_width=True)

        # Survival curves
        st.subheader("Survival Curves")
        cohorts_df['survival'] = 1 - cohorts_df['retention_rate']
        fig = px.line(cohorts_df, x="period_number", y="survival",
                      color="cohort_period", title="Survival Curves (Churn Probability)")
        st.plotly_chart(fig, use_container_width=True)

        # Cohort comparison at a specific period
        st.subheader("Cohort Comparison")
        period_filter = st.slider("Select Period Number", 0, 12, 4)
        filtered = cohorts_df[cohorts_df['period_number'] == period_filter]
        if not filtered.empty:
            fig = px.bar(filtered, x="cohort_period", y="retention_rate",
                         title=f"Retention Rate at Period {period_filter}")
            st.plotly_chart(fig, use_container_width=True)

    finally:
        session.close()