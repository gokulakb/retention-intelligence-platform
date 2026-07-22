"""
Reusable chart functions using Plotly and Altair.
"""
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import numpy as np

def plotly_line_chart(df, x, y, title="", color=None):
    """Create a line chart."""
    fig = px.line(df, x=x, y=y, title=title, color=color)
    return fig

def plotly_bar_chart(df, x, y, title="", color=None, barmode='group'):
    """Create a bar chart."""
    fig = px.bar(df, x=x, y=y, title=title, color=color, barmode=barmode)
    return fig

def plotly_heatmap(df, title="", xlabel="", ylabel="", color_continuous_scale="Blues"):
    """
    Create a heatmap from a pivot table (DataFrame with index = rows, columns = periods).
    """
    # Replace NaN with 0 for cleaner display
    df_clean = df.fillna(0)
    fig = px.imshow(
        df_clean,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=color_continuous_scale,
        title=title,
        labels=dict(x=xlabel, y=ylabel, color="Retention Rate")
    )
    fig.update_xaxes(tickangle=45)  # rotate x labels if many periods
    return fig

def plotly_pie_chart(df, names, values, title=""):
    """Create a pie chart."""
    fig = px.pie(df, names=names, values=values, title=title)
    return fig

def plotly_scatter(df, x, y, color=None, size=None, title=""):
    """Create a scatter plot."""
    fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title)
    return fig

def plotly_correlation_matrix(df, title="Correlation Matrix"):
    """Plot correlation matrix."""
    corr = df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r",
                    title=title)
    return fig

def altair_bar_chart(df, x, y, title=""):
    """Create an Altair bar chart."""
    chart = alt.Chart(df).mark_bar().encode(
        x=x,
        y=y,
        tooltip=[x, y]
    ).properties(title=title)
    return chart