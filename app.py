"""
Retention Intelligence & Cohort Analytics Platform
Main application entry point.
"""
import streamlit as st
from streamlit_option_menu import option_menu
import os
from pathlib import Path

# Page imports
from dashboard.overview import overview_page
from dashboard.executive_dashboard import executive_dashboard
from dashboard.cohort_dashboard import cohort_dashboard
from dashboard.churn_dashboard import churn_dashboard
from dashboard.behavior_dashboard import behavior_dashboard
from dashboard.recommendations import recommendations_page
from reports.export import report_export_page

# Configuration
st.set_page_config(
    page_title="Retention Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
def load_css():
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2563EB;
        }
        .kpi-card {
            background: #F3F4F6;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1E3A8A;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #6B7280;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    load_css()

    # Sidebar navigation
    with st.sidebar:
        # Try to display logo; fallback to title if file missing
        logo_path = Path("assets/logo.png")
        if logo_path.exists():
            st.image(str(logo_path), width=200)
        else:
            st.markdown("## 📊 Retention Intelligence")
        
        st.markdown("## Navigation")
        selected = option_menu(
            menu_title=None,
            options=[
                "Home",
                "Executive Dashboard",
                "Cohort Analysis",
                "Churn Analysis",
                "Behavioral Insights",
                "Predictive Analytics",
                "Reports"
            ],
            icons=[
                "house",
                "speedometer2",
                "grid",
                "graph-down",
                "person-workspace",
                "brain",
                "file-earmark-pdf"
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#1E3A8A", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#2563EB"},
            }
        )

    # Route to selected page
    if selected == "Home":
        overview_page()
    elif selected == "Executive Dashboard":
        executive_dashboard()
    elif selected == "Cohort Analysis":
        cohort_dashboard()
    elif selected == "Churn Analysis":
        churn_dashboard()
    elif selected == "Behavioral Insights":
        behavior_dashboard()
    elif selected == "Predictive Analytics":
        recommendations_page()
    elif selected == "Reports":
        report_export_page()

if __name__ == "__main__":
    main()