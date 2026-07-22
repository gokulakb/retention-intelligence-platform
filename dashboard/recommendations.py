"""
Predictive Analytics & Recommendations page.
"""
import streamlit as st
import pandas as pd
from database.database import SessionLocal
from models.retention_model import train_retention_models, get_retention_probability
from models.churn_model import get_churn_risk_users
from models.feature_importance import get_feature_importance
import plotly.express as px

def recommendations_page():
    st.markdown('<div class="main-header">Predictive Analytics & Recommendations</div>',
                unsafe_allow_html=True)

    session = SessionLocal()
    try:
        # Train models
        if st.button("Train Retention Models"):
            with st.spinner("Training models..."):
                results, models, features = train_retention_models(session)
                if results:
                    st.success("Models trained successfully!")
                    st.subheader("Model Evaluation Metrics")
                    df_metrics = pd.DataFrame(results).T
                    st.dataframe(df_metrics)
                else:
                    st.error("Training failed. Insufficient data.")

        # Predict for a specific user
        st.subheader("Predict Retention for a User")
        user_id = st.text_input("Enter User ID")
        if user_id:
            prob = get_retention_probability(session, user_id)
            if prob is not None:
                st.metric("Retention Probability", f"{prob:.1%}")
            else:
                st.warning("User not found or model not trained yet.")

        # High‑risk churn users
        st.subheader("High‑Risk Churn Users")
        risk_users = get_churn_risk_users(session)
        if not risk_users.empty:
            st.dataframe(risk_users[['user_id', 'email', 'user_type',
                                     'last_active', 'days_active']])
        else:
            st.info("No high‑risk users currently.")

        # Feature importance (re‑display)
        st.subheader("Feature Importance")
        imp_df = get_feature_importance(session)
        if not imp_df.empty:
            fig = px.bar(imp_df, x='feature', y='importance',
                         title="Feature Importance for Retention")
            st.plotly_chart(fig, use_container_width=True)

        # Actionable recommendations
        st.subheader("Actionable Recommendations")
        st.markdown("""
        - **Low profile completion** → send prompts to complete profiles.
        - **Low session count** → share engaging content or notifications.
        - **High churn risk** → offer incentives, re‑engagement campaigns.
        - **Focus on high‑importance features** (e.g., applications, sessions) to improve retention.
        """)

    finally:
        session.close()