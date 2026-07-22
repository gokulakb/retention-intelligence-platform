"""
Report export page – CSV, Excel, PDF.
"""
import streamlit as st
import pandas as pd
from io import BytesIO
from database.database import SessionLocal
from reports.csv_export import export_csv
from reports.pdf_generator import generate_pdf

def report_export_page():
    st.markdown('<div class="main-header">Reports & Exports</div>', unsafe_allow_html=True)

    session = SessionLocal()
    try:
        report_type = st.selectbox(
            "Select Report Type",
            ["User Data", "Retention Metrics", "Churn Analysis", "Behavioral Features"]
        )

        if report_type == "User Data":
            from database.queries import get_users
            df = get_users(session)
        elif report_type == "Retention Metrics":
            from database.queries import get_retention_metrics
            df = get_retention_metrics(session)
        elif report_type == "Churn Analysis":
            from analytics.churn_analysis import churn_trend
            df = churn_trend(session)
        else:  # Behavioral Features
            from analytics.behavioral_analysis import compute_behavioral_features
            df = compute_behavioral_features(session)

        if df.empty:
            st.warning("No data available for this report.")
            return

        st.dataframe(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                data=csv,
                file_name=f"{report_type.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        with col2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Report')
            st.download_button(
                "Download Excel",
                data=output.getvalue(),
                file_name=f"{report_type.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with col3:
            pdf_bytes = generate_pdf(df, title=report_type)
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=f"{report_type.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )

    finally:
        session.close()