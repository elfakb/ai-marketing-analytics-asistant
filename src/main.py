from data_loader import load_campaign_data, get_best_and_worst_campaign
from charts import plot_roas_by_campaign, plot_spend_vs_revenue
from ai import get_ai_insights
from report_builder import build_report


def run_pipeline(csv_path: str = "../data/campaigns_sample.csv"):
    print("Step 1: Loading and analyzing campaign data...")
    df = load_campaign_data(csv_path)
    print(df[["Campaign", "CTR", "CPC", "CPA", "Conversion_Rate", "ROAS"]])

    print("\nStep 2: Identifying best and worst campaigns...")
    best, worst = get_best_and_worst_campaign(df)
    print(f"Best (ROAS): {best['Campaign']} -> {best['ROAS']}")
    print(f"Worst (CPA): {worst['Campaign']} -> ${worst['CPA']}")

    print("\nStep 3: Generating charts...")
    chart1 = plot_roas_by_campaign(df, "../outputs/charts/roas_by_campaign.png")
    chart2 = plot_spend_vs_revenue(df, "../outputs/charts/spend_vs_revenue.png")
    print(f"Saved: {chart1}")
    print(f"Saved: {chart2}")

    print("\nStep 4: Requesting AI insights...")
    insights = get_ai_insights(df, best, worst)
    print("AI insights received.")

    print("\nStep 5: Building PDF report...")
    report_path = build_report(
        df, best, worst, insights,
        [chart1, chart2],
        output_path="../outputs/reports/weekly_report.pdf"
    )
    print(f"\n✅ Done! Report saved to: {report_path}")


if __name__ == "__main__":
    run_pipeline()