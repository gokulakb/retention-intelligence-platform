"""
Application settings: churn, retention, cohorts, and colors.
All business rules are centralised here for easy tuning.
"""

# =============================================================================
# CHURN DEFINITION
# =============================================================================
# Number of consecutive days of inactivity after which a user is considered churned.
# Example: 30 (standard), 45 (for B2B SaaS), 14 (for high‑velocity apps)
CHURN_INACTIVITY_DAYS = 30

# =============================================================================
# RETENTION WINDOWS (in days)
# =============================================================================
# Periods at which retention is measured (from signup).
# Used in cohort analysis and KPI calculations.
# Example: [7, 30, 60, 90] (weekly, monthly, 2‑month, 3‑month)
RETENTION_WINDOWS = [7, 30, 60, 90, 180, 365]

# =============================================================================
# COHORT GROUPING PERIODS
# =============================================================================
# How users are grouped by signup time.
# Allowed values: "weekly", "monthly", "daily"
COHORT_PERIODS = ["weekly", "monthly"]   # you can add "daily" if needed

# =============================================================================
# BEHAVIORAL FEATURES (used in analytics & ML models)
# =============================================================================
# The list of behavioral columns expected in the users table.
# If your production data has different names, adjust accordingly.
BEHAVIORAL_FEATURES = [
    "profile_completion",
    "total_sessions",
    "applications_submitted",
    "searches_performed",
    "messages_sent",
    "saved_opportunities",
    "session_duration_avg",
    "days_active",
    "time_to_first_action"
]

# =============================================================================
# COLOR PALETTE (for dashboards)
# =============================================================================
COLOR_PALETTE = {
    "primary": "#1E3A8A",
    "secondary": "#2563EB",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3B82F6",
    "light": "#F3F4F6",
    "dark": "#1F2937",
}