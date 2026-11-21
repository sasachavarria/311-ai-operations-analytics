import requests
from analysis import (
    get_overview,
    get_top_categories,
    get_monthly_trends,
    get_top_neighbourhoods,
    get_status_breakdown
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def get_analytics_context():
    overview = get_overview().to_string(index=False)
    categories = get_top_categories().to_string(index=False)
    monthly = get_monthly_trends().tail(12).to_string(index=False)
    neighbourhoods = get_top_neighbourhoods().to_string(index=False)
    statuses = get_status_breakdown().to_string(index=False)

    context = f"""
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

    return context


def ask_ai(question, context=None):
    if context is None:
        context = get_analytics_context()

    prompt = f"""
    You are a data analyst examining Edmonton 311 service request data.

    Answer the user's question using ONLY the supplied data.

    Rules:
    - Do not invent statistics or figures.
    - If the data does not contain the answer, say so.
    - Identify meaningful trends and patterns.
    - Explain findings in clear, professional language.
    - Keep the answer concise and useful for decision-making.

    DATA:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()["response"]


if __name__ == "__main__":
    print(get_analytics_context())
    print("\nAI ANALYST TEST:")
    print(ask_ai("What are the main patterns in this dataset?"))
