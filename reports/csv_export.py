"""
CSV export utility.
"""
import pandas as pd

def export_csv(df: pd.DataFrame, filepath: str) -> None:
    """Export a DataFrame to a CSV file."""
    df.to_csv(filepath, index=False)