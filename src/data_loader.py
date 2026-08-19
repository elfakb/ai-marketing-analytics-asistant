import pandas as pd


def load_campaign_data(csv_path: str) -> pd.DataFrame:
    """Reads the CSV and computes all performance metrics, returning a DataFrame."""
    df = pd.read_csv(csv_path)

    # Core metrics
    df["CTR"] = (df["Clicks"] / df["Impressions"]) * 100              # %
    df["CPC"] = df["Spend"] / df["Clicks"]                            # cost per click
    df["CPA"] = df["Spend"] / df["Conversions"]                       # cost per acquisition
    df["Conversion_Rate"] = (df["Conversions"] / df["Clicks"]) * 100  # %
    df["ROAS"] = df["Revenue"] / df["Spend"]                          # return on ad spend

    # Round for readability
    df = df.round({
        "CTR": 2,
        "CPC": 2,
        "CPA": 2,
        "Conversion_Rate": 2,
        "ROAS": 2
    })

    return df


def get_best_and_worst_campaign(df: pd.DataFrame):
    """Finds the campaign with the highest ROAS (best) and highest CPA (worst)."""
    best_campaign = df.loc[df["ROAS"].idxmax()]
    worst_campaign = df.loc[df["CPA"].idxmax()]
    return best_campaign, worst_campaign


if __name__ == "__main__":
    # Quick test run
    df = load_campaign_data("data/campaigns_sample.csv")
    print(df)

    best, worst = get_best_and_worst_campaign(df)
    print("\n🏆 Best performing campaign (ROAS):")
    print(best[["Campaign", "ROAS"]])

    print("\n⚠️ Worst performing campaign (CPA):")
    print(worst[["Campaign", "CPA"]])