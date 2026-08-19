import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_roas_by_campaign(df: pd.DataFrame, output_path: str = "outputs/charts/roas_by_campaign.png"):
    """Bar chart showing ROAS for each campaign."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_sorted = df.sort_values("ROAS", ascending=False)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(df_sorted["Campaign"], df_sorted["ROAS"], color="#4C72B0")

    plt.title("ROAS by Campaign", fontsize=14, fontweight="bold")
    plt.xlabel("Campaign")
    plt.ylabel("ROAS (Revenue / Spend)")
    plt.xticks(rotation=45, ha="right")
    plt.axhline(y=1, color="red", linestyle="--", linewidth=1, label="Break-even (ROAS = 1)")
    plt.legend()

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
                  f"{height:.2f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def plot_spend_vs_revenue(df: pd.DataFrame, output_path: str = "outputs/charts/spend_vs_revenue.png"):
    """Grouped bar chart comparing Spend vs Revenue per campaign."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_sorted = df.sort_values("Revenue", ascending=False)

    x = range(len(df_sorted))
    width = 0.35

    plt.figure(figsize=(11, 6))
    plt.bar([i - width/2 for i in x], df_sorted["Spend"], width, label="Spend", color="#DD8452")
    plt.bar([i + width/2 for i in x], df_sorted["Revenue"], width, label="Revenue", color="#55A868")

    plt.title("Spend vs Revenue by Campaign", fontsize=14, fontweight="bold")
    plt.xlabel("Campaign")
    plt.ylabel("Amount ($)")
    plt.xticks(list(x), df_sorted["Campaign"], rotation=45, ha="right")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


if __name__ == "__main__":
    from data_loader import load_campaign_data

    df = load_campaign_data("data/campaigns_sample.csv")

    path1 = plot_roas_by_campaign(df)
    path2 = plot_spend_vs_revenue(df)

    print(f"Saved: {path1}")
    print(f"Saved: {path2}")