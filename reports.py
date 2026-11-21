
import os
import pandas as pd
import plotly.express as px

from analysis import get_monthly_trends, get_top_categories


def detect_anomalies():

    monthly = get_monthly_trends().copy()

    monthly["period"] = (
        monthly["year"].astype(str)
        + "-"
        + monthly["month_number"].astype(str).str.zfill(2)
    )

    monthly = monthly.sort_values(
        ["year", "month_number"]
    ).reset_index(drop=True)

    monthly["previous_average"] = (
        monthly["total_requests"]
        .shift(1)
        .rolling(window=3, min_periods=3)
        .mean()
    )

    monthly["previous_std"] = (
        monthly["total_requests"]
        .shift(1)
        .rolling(window=3, min_periods=3)
        .std()
    )

    monthly["anomaly"] = (
        monthly["total_requests"]
        > monthly["previous_average"]
        + 2 * monthly["previous_std"]
    )

    return monthly


def generate_report():

    monthly = detect_anomalies()
    categories = get_top_categories()

    anomalies = monthly[monthly["anomaly"]]

    os.makedirs("reports", exist_ok=True)

    fig = px.line(
        monthly,
        x="period",
        y="total_requests",
        markers=True,
        title="Monthly Service Request Volumes"
    )

    if not anomalies.empty:
        fig.add_scatter(
            x=anomalies["period"],
            y=anomalies["total_requests"],
            mode="markers",
            name="Potential anomalies",
            marker={"size": 12, "symbol": "x"}
        )

    report = f"""
    <html>
    <head>
        <title>Edmonton 311 Operations Report</title>
    </head>
    <body>
        <h1>Edmonton 311 Operations Report</h1>

        <h2>Report Summary</h2>

        <p>
        This report summarizes monthly service request volumes,
        identifies potential unusual increases, and highlights
        the most common service categories.
        </p>

        <h2>Potential Anomalies</h2>

        {anomalies.to_html(index=False)}

        <h2>Top Service Categories</h2>

        {categories.to_html(index=False)}

        <h2>Monthly Trends</h2>

        {fig.to_html(full_html=False, include_plotlyjs="cdn")}

    </body>
    </html>
    """

    output_path = "reports/monthly_operations_report.html"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)

    return output_path


if __name__ == "__main__":
    path = generate_report()
    print(f"Report generated: {path}")
