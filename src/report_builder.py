from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib import colors
import os
from datetime import datetime


def build_report(df, best_campaign, worst_campaign, ai_insights: str,
                  chart_paths: list, output_path: str = "outputs/reports/weekly_report.pdf"):
    """Combines metrics table, charts, and AI insights into a single PDF report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm,
                             leftMargin=1.5*cm, rightMargin=1.5*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=20)
    heading_style = ParagraphStyle("HeadingStyle", parent=styles["Heading2"], spaceBefore=14, spaceAfter=8)
    body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontSize=10, leading=14)

    elements = []

    # Title
    elements.append(Paragraph("Campaign Performance Report", title_style))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d')}", body_style))
    elements.append(Spacer(1, 0.5*cm))

    # Summary highlights
    elements.append(Paragraph("Highlights", heading_style))
    elements.append(Paragraph(
        f"<b>Best performing campaign:</b> {best_campaign['Campaign']} (ROAS: {best_campaign['ROAS']})",
        body_style
    ))
    elements.append(Paragraph(
        f"<b>Most costly campaign:</b> {worst_campaign['Campaign']} (CPA: ${worst_campaign['CPA']})",
        body_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    # Metrics table
    elements.append(Paragraph("Campaign Metrics", heading_style))
    table_data = [["Campaign", "Spend", "Revenue", "CTR%", "CPC", "CPA", "Conv%", "ROAS"]]
    for _, row in df.iterrows():
        table_data.append([
            row["Campaign"], f"${row['Spend']}", f"${row['Revenue']}",
            row["CTR"], f"${row['CPC']}", f"${row['CPA']}",
            row["Conversion_Rate"], row["ROAS"]
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C72B0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.7*cm))

    # Charts
    elements.append(Paragraph("Charts", heading_style))
    for chart_path in chart_paths:
        if os.path.exists(chart_path):
            elements.append(Image(chart_path, width=16*cm, height=9*cm))
            elements.append(Spacer(1, 0.5*cm))

    # AI Insights
    elements.append(Paragraph("AI-Generated Insights & Recommendations", heading_style))
    for line in ai_insights.split("\n"):
        if line.strip():
            elements.append(Paragraph(line.strip(), body_style))
        else:
            elements.append(Spacer(1, 0.2*cm))

    doc.build(elements)
    return output_path


if __name__ == "__main__":
    from data_loader import load_campaign_data, get_best_and_worst_campaign
    from charts import plot_roas_by_campaign, plot_spend_vs_revenue
    from ai import get_ai_insights

    df = load_campaign_data("data/campaigns_sample.csv")
    best, worst = get_best_and_worst_campaign(df)

    chart1 = plot_roas_by_campaign(df)
    chart2 = plot_spend_vs_revenue(df)

    insights = get_ai_insights(df, best, worst)

    report_path = build_report(df, best, worst, insights, [chart1, chart2])
    print(f"Report saved to: {report_path}")