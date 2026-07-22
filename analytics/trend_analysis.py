"""
Trend analysis: moving averages, decomposition, and growth rate calculations.
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sqlalchemy.orm import Session
from analytics.churn_analysis import churn_trend
import logging

logger = logging.getLogger(__name__)

def compute_moving_average(series: pd.Series, window: int = 4):
    """Compute simple moving average."""
    return series.rolling(window=window).mean()

def compute_growth_rate(series: pd.Series):
    """Compute percentage growth from previous period."""
    return series.pct_change() * 100

def trend_decomposition(session: Session, user_type: str = None, period: int = 4):
    """
    Decompose churn trend into trend, seasonal, and residual components.
    Requires at least 2*period data points.
    """
    trend_df = churn_trend(session, user_type)
    if trend_df.empty or len(trend_df) < 2 * period:
        logger.warning("Insufficient data for decomposition.")
        return None

    # Set period as index
    ts = trend_df.set_index('period')['churn_rate']
    ts = ts.asfreq('W-MON')  # weekly frequency
    # Fill missing
    ts = ts.fillna(method='ffill')
    if len(ts) < 2 * period:
        return None
    decomposition = seasonal_decompose(ts, model='additive', period=period)
    return decomposition