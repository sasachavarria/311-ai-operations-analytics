
import requests
from analysis import (
    get_overview,
    get_top_categories,
    get_monthly_trends,
    get_top_neighbourhoods,
    get_status_breakdown
)
PROMPT = """You are a helpful data analyst explaining Edmonton 311 service request data
to a non-technical person.

You are NOT a SQL assistant or a programming assistant.

The user wants an explanation of the data, not code.

IMPORTANT INSTRUCTIONS:
- Answer in plain, natural English.
- Do not write SQL queries.
- Do not write Python code.
- Do not use code blocks.
- Do not explain how to query a database.
- Use only facts and numbers shown in the database results.
- Do not invent statistics or calculate new numerical values.
- If the data does not answer the question, say that clearly.
- Keep your answer concise and easy to understand.
- You may explain what the results could mean, but label suggestions as recommendations.
- Respond in plain english.
- Include in your answer how many lines of data you receive.
"""

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def get_analytics_context():
    overview = get_overview().to_string(index=False)
    categories = get_top_categories().to_string(index=False)
    monthly = get_monthly_trends().tail(12).to_string(index=False)
    neighbourhoods = get_top_neighbourhoods().to_string(index=False)
    statuses = get_status_breakdown().to_string(index=False)

    return f"""
DATABASE RESULTS:

OVERVIEW:
{overview}

TOP SERVICE CATEGORIES:
{categories}

LAST 12 MONTHLY RECORDS:
{monthly}

TOP NEIGHBOURHOODS:
{neighbourhoods}

REQUEST STATUSES:
{statuses}
"""


def build_analytics_context(data):

    if data.empty:
        return "No data is available for the selected filters."

    total = data["total_requests"].sum()

    monthly = (
        data.groupby(
            ["year", "month_number", "month"],
            as_index=False
        )["total_requests"]
        .sum()
        .sort_values(["year", "month_number"])
    )

    annual_peaks = monthly.loc[
        monthly.groupby("year")["total_requests"].idxmax()
    ]

    categories = (
        data.groupby("service_category")["total_requests"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    neighbourhoods = (
        data.groupby("neighbourhood")["total_requests"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    statuses = (
        data.groupby("request_status")["total_requests"]
        .sum()
        .sort_values(ascending=False)
    )

    return f"""
TOTAL REQUESTS: {total:,.0f}

MONTHLY TOTALS (ALL AVAILABLE MONTHS):
{monthly.to_string(index=False)}

HIGHEST MONTH BY YEAR:
{annual_peaks.to_string(index=False)}

TOP 10 CATEGORIES:
{categories.to_string()}

TOP 10 NEIGHBOURHOODS:
{neighbourhoods.to_string()}

REQUEST STATUSES:
{statuses.to_string()}
"""

def ask_ai(question, context=None):
    if context is None:
        context = get_analytics_context()

    prompt = f"""

Here are the database results:
{context}

The user's question is:
{question}

Respond directly to the user's question in plain English.
"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "system": PROMPT,
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        },
        timeout=180
    )

    response.raise_for_status()

    answer = response.json()["response"].strip()
    used = response.json().get("prompt_eval_count", 0)
    note = f"\n\n---\nModel read {used:,} of 8,192 prompt tokens."
    if used >= 8192 - 50:
        note += "\n\nWarning: prompt was likely truncated."

    return answer + note


if __name__ == "__main__":
    print("\nAI ANALYST TEST:")
    print(ask_ai("What are the main patterns in this dataset?"))
    
