"""
Churn Analytics Dashboard page.
"""
import streamlit as st
import pandas as pd
from database.database import SessionLocal
from analytics.churn_analysis import compute_churn_rate, churn_trend, high_risk_users
import plotly.express as px

def churn_dashboard():
    st.markdown('<div class="main-header">Churn Analytics</div>', unsafe_allow_html=True)

    session = SessionLocal()
    try:
        col1, col2 = st.columns(2)
        with col1:
            user_type = st.selectbox("User Type", ["all", "candidate", "company"], index=0)
            if user_type == "all":
                user_type = None
        with col2:
            days_inactive = st.slider("Inactivity threshold (days)", 7, 90, 30)

        # Current churn rate
        churn_info = compute_churn_rate(session, user_type, days_inactive)
        st.metric("Current Churn Rate", f"{churn_info['churn_rate']:.1%}",
                  f"{churn_info['churned']} churned out of {churn_info['total']}")

        # Churn trend
        st.subheader("Churn Trend Over Time")
        trend_df = churn_trend(session, user_type, days_inactive)
        if not trend_df.empty:
            fig = px.line(trend_df, x='period', y='churn_rate',
                          title="Weekly Churn Rate")
            st.plotly_chart(fig, use_container_width=True)

        # High-risk users
        st.subheader("High‑Risk Users")
        risk_df = high_risk_users(session, days_inactive_threshold=days_inactive,
                                  user_type=user_type)
        if not risk_df.empty:
            st.dataframe(risk_df[['user_id', 'email', 'user_type',
                                  'last_active', 'days_active']])
            st.info(f"Found {len(risk_df)} users at high risk of churn.")
        else:
            st.success("No high‑risk users found.")

        # Churn by user type
        st.subheader("Churn Rate by User Type")
        churn_by_type = {}
        for ut in ['candidate', 'company']:
            res = compute_churn_rate(session, ut, days_inactive)
            churn_by_type[ut] = res['churn_rate']
        df_type = pd.DataFrame(list(churn_by_type.items()),
                               columns=['User Type', 'Churn Rate'])
        fig = px.bar(df_type, x='User Type', y='Churn Rate',
                     title="Churn Rate by User Type")
        st.plotly_chart(fig, use_container_width=True)

    finally:
        session.close()