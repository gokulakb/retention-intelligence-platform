"""
Formatting utilities for display.
"""
def kpi_card(value, label, delta=None, delta_color="normal"):
    """Return a formatted KPI card (as HTML string)."""
    delta_html = ""
    if delta is not None:
        sign = "+" if delta > 0 else ""
        color = "green" if delta > 0 else "red"
        delta_html = f'<span style="color:{color};">{sign}{delta:.1f}%</span>'
    html = f"""
    <div class="kpi-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """
    return html