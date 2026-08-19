import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(df, best_campaign, worst_campaign) -> str:
    """Turns the calculated metrics into a text prompt for the AI."""
    summary_lines = []
    for _, row in df.iterrows():
        summary_lines.append(
            f"- {row['Campaign']}: Spend=${row['Spend']}, Revenue=${row['Revenue']}, "
            f"CTR={row['CTR']}%, CPC=${row['CPC']}, CPA=${row['CPA']}, "
            f"Conversion Rate={row['Conversion_Rate']}%, ROAS={row['ROAS']}"
        )
    data_summary = "\n".join(summary_lines)

    prompt = f"""
You are a digital marketing analyst reviewing campaign performance data.

Here is the performance data for all campaigns:
{data_summary}

Best performing campaign (highest ROAS): {best_campaign['Campaign']} (ROAS: {best_campaign['ROAS']})
Worst performing campaign (highest CPA): {worst_campaign['Campaign']} (CPA: ${worst_campaign['CPA']})

Based on this data, provide:
1. Three concrete, actionable recommendations to improve overall campaign performance.
2. Which campaign(s) should get increased budget, and why.
3. Which campaign(s) should be paused or reduced, and why.

Keep the response concise, data-driven, and formatted with clear headers.
"""
    return prompt.strip()


def get_ai_insights(df, best_campaign, worst_campaign, model: str = "gpt-4o-mini") -> str:
    """Sends the prompt to the OpenAI API and returns the AI-generated insights."""
    prompt = build_prompt(df, best_campaign, worst_campaign)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful and analytical digital marketing consultant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from data_loader import load_campaign_data, get_best_and_worst_campaign

    df = load_campaign_data("data/campaigns_sample.csv")
    best, worst = get_best_and_worst_campaign(df)

    insights = get_ai_insights(df, best, worst)
    print(insights)