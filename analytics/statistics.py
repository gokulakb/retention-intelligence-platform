"""
Statistical tests for comparing retention between groups.
"""
import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from database.queries import get_users

def t_test_retention_by_group(session: Session, group_col: str, group_values: list):
    """
    Perform independent t-test on retention (days_active) between two groups.
    group_col: column name (e.g., 'user_type')
    group_values: list of two values to compare (e.g., ['candidate', 'company'])
    Returns t-statistic and p-value.
    """
    users_df = get_users(session)
    if users_df.empty:
        return None, None

    group1 = users_df[users_df[group_col] == group_values[0]]['days_active'].dropna()
    group2 = users_df[users_df[group_col] == group_values[1]]['days_active'].dropna()
    if len(group1) < 2 or len(group2) < 2:
        return None, None
    t_stat, p_val = stats.ttest_ind(group1, group2)
    return t_stat, p_val

def anova_retention_by_cluster(session: Session, cluster_col: str = 'cluster'):
    """
    Perform one-way ANOVA to test if retention (days_active) differs across clusters.
    Returns F-statistic and p-value.
    """
    from analytics.segmentation import segment_users
    seg_df = segment_users(session)
    if seg_df.empty or cluster_col not in seg_df.columns:
        return None, None

    groups = [group['days_active'].dropna().values for name, group in seg_df.groupby(cluster_col)]
    if len(groups) < 2:
        return None, None
    f_stat, p_val = stats.f_oneway(*groups)
    return f_stat, p_val