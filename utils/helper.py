"""
General helper functions.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def date_range(start, end, freq='D'):
    """Generate date range."""
    return pd.date_range(start=start, end=end, freq=freq)

def safe_divide(a, b):
    """Safe division, returns 0 if b=0."""
    return a / b if b != 0 else 0.0

def round_to_nearest(value, base=5):
    """Round to nearest multiple of base."""
    return round(value / base) * base

def calculate_growth_rate(current, previous):
    """Compute growth rate as percentage."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def format_percentage(value, decimals=1):
    """Format as percentage string."""
    return f"{value:.{decimals}f}%"