
import streamlit as st
import pandas as pd
import plotly.express as px

from analysis import (
    get_overview,
    get_top_categories,
    get_monthly_trends,
    get_top_neighbourhoods,
    get_status_breakdown,
    get_service_areas,
    get_filter_options,
    get_filtered_data
)

from ai_analyst import ask_ai

st.set_page_config(
    page_title="Edmonton 311 Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Edmonton 311 Analytics")
st.caption("AI-powered municipal service request intelligence")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

try:
    years, categories, neighbourhoods = get_filter_options()

    selected_years = st.sidebar.multiselect(
        "Select years",
        years,
        default=years
    )

    selected_categories = st.sidebar.multiselect(
        "Service categories",
        categories
    )

    selected_neighbourhoods = st.sidebar.multiselect(
        "Neighbourhoods",
        neighbourhoods
    )

    data = get_filtered_data(
        selected_years,
        selected_categories,
        selected_neighbourhoods
    )

except Exception as error:
    st.error(f"Could not load dashboard filters: {error}")
    st.stop()

# Overview
st.header("Operational Overview")

total_requests = data["total_requests"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Filtered Requests", f"{total_requests:,.0f}")
col2.metric("Years Selected", len(selected_years))
col3.metric("Categories Found", data["service_category"].nunique())

st.divider()

# Monthly trends
st.subheader("Monthly Request Trends")

monthly = (
    data.groupby(["year", "month_number"], as_index=False)
    ["total_requests"].sum()
)

monthly["period"] = (
    monthly["year"].astype(str)
    + "-"
    + monthly["month_number"].astype(str).str.zfill(2)
)

fig_monthly = px.line(
    monthly,
    x="period",
    y="total_requests",
    markers=True,
    title="Requests Over Time"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# Category and neighbourhood charts
col1, col2 = st.columns(2)

with col1:

    category_data = (
        data.groupby("service_category", as_index=False)
        ["total_requests"].sum()
        .sort_values("total_requests", ascending=False)
        .head(10)
    )

    fig_categories = px.bar(
        category_data,
        x="total_requests",
        y="service_category",
        orientation="h",
        title="Top Service Categories"
    )

    fig_categories.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_categories, use_container_width=True)

with col2:

    neighbourhood_data = (
        data.groupby("neighbourhood", as_index=False)
        ["total_requests"].sum()
        .sort_values("total_requests", ascending=False)
        .head(10)
    )

    fig_neighbourhoods = px.bar(
        neighbourhood_data,
        x="total_requests",
        y="neighbourhood",
        orientation="h",
        title="Top Neighbourhoods"
    )

    fig_neighbourhoods.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_neighbourhoods, use_container_width=True)

# Status breakdown
st.subheader("Request Status")

status_data = (
    data.groupby("request_status", as_index=False)
    ["total_requests"].sum()
)

fig_status = px.pie(
    status_data,
    names="request_status",
    values="total_requests",
    hole=0.4
)

st.plotly_chart(fig_status, use_container_width=True)

# Raw data
with st.expander("Explore filtered records"):
    st.dataframe(data, use_container_width=True)

# AI Analyst
st.divider()

st.header("AI Operations Analyst")

st.write(
    "Ask questions about municipal service requests "
    "and receive AI-generated analytical insights."
)

question = st.text_area(
    "Your question",
    placeholder="Which service categories are increasing?"
)

if st.button("Generate AI Analysis"):

    if not question.strip():
        st.warning("Enter a question first.")

    else:
        with st.spinner("Analyzing your data..."):

            try:
                answer = ask_ai(question, context=data.to_string(index=False))
                st.markdown(answer)

            except Exception as error:
                st.error(f"AI analysis failed: {error}")
