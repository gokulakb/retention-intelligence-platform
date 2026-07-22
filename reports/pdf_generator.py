"""
PDF report generator using FPDF.
"""
from fpdf import FPDF
import pandas as pd

def generate_pdf(df: pd.DataFrame, title: str = "Report") -> bytes:
    """
    Generate a simple PDF from a DataFrame.
    Returns the PDF as bytes for download.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)

    # Table header
    pdf.set_font("Arial", 'B', 10)
    cols = df.columns
    for col in cols:
        pdf.cell(30, 10, str(col), border=1)
    pdf.ln()

    # Table rows (limit to first 100)
    pdf.set_font("Arial", size=8)
    for _, row in df.head(100).iterrows():
        for col in cols:
            pdf.cell(30, 10, str(row[col])[:20], border=1)
        pdf.ln()

    # Return as bytes
    return pdf.output(dest='S').encode('latin-1')