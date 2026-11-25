
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

from ai_analyst import ask_ai, build_analytics_context

st.set_page_config(
    page_title="Edmonton 311 Analytics",
    page_icon="📊",
    layout="wide"
)


# Dashboard styling
st.markdown("""
<style>
/* Main page */
.stApp {
    background-color: #F4F6F9;
    color: #243247 !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #F4F6F9;
    color: #243247 !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Force readable dark text throughout the dashboard */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp label,
.stApp li,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stCaptionContainer"] p,
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricDelta"] {
    color: #243247 !important;
}

/* Title */
h1 {
    color: #17365C !important;
    font-weight: 750 !important;
    letter-spacing: -0.8px;
}

h2, h3 {
    color: #24466B !important;
    font-weight: 650 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #E9EEF4;
}

[data-testid="stSidebar"] * {
    color: #243247 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EB;
    border-radius: 10px;
    padding: 18px 20px;
}

[data-testid="stMetricLabel"] {
    color: #52657B !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #17365C !important;
    font-size: 28px !important;
    font-weight: 750 !important;
}

/* Chart containers */
[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EB;
    border-radius: 10px;
    padding: 8px;
}

/* Inputs */
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #243247 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px;
}

.stTextArea textarea::placeholder {
    color: #8491A2 !important;
}

/* Buttons */
.stButton > button {
    background-color: #244F78 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 7px;
    padding: 0.55rem 1.3rem;
    font-weight: 650;
}

.stButton > button:hover {
    background-color: #0F766E !important;
    color: #FFFFFF !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EB;
    border-radius: 9px;
}

/* Dividers */
hr {
    border-color: #DCE3EB !important;
}


/* Light header */
[data-testid="stHeader"],
.stAppHeader {
    background-color: #F5F7F8 !important;
}

/* Softer sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background-color: #EAF1EF !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #263B48 !important;
}

/* Filter dropdowns */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #D4DFDC !important;
    color: #263B48 !important;
}

/* Selected filter tags */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #D7EBE5 !important;
    color: #17675D !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] * {
    color: #17675D !important;
}

/* Selected dropdown options */
[role="option"][aria-selected="true"] {
    background-color: #E4F1ED !important;
    color: #17675D !important;
}

/* Accent buttons */
.stButton > button {
    background-color: #167D72 !important;
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: #11665D !important;
    color: #FFFFFF !important;
}


</style>
""", unsafe_allow_html=True)


# Consistent Plotly styling
def style_chart(fig, height=360):

    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#243247"
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=30, t=65, b=40),
        title=dict(
            font=dict(
                size=17,
                color="#17365C"
            ),
            x=0.02,
            xanchor="left"
        ),
        hoverlabel=dict(
            bgcolor="#17365C",
            font_color="#FFFFFF"
        ),
        legend=dict(
            font=dict(
                color="#243247",
                size=11
            ),
            bgcolor="#FFFFFF"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        title=None,
        tickfont=dict(color="#52657B")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E8EDF2",
        zeroline=False,
        showline=False,
        title=None,
        tickfont=dict(color="#52657B")
    )

    return fig


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

fig_monthly.update_traces(
    line=dict(
        color="#0F766E",
        width=3
    ),
    marker=dict(
        size=7,
        color="#0F766E",
        line=dict(color="#FFFFFF", width=1.5)
    ),
    hovertemplate="%{x}<br>Requests: %{y:,.0f}<extra></extra>"
)

style_chart(fig_monthly, 380)

fig_monthly.update_layout(
    hovermode="x unified"
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
        title="Top Service Categories",
        text="total_requests",
        color_discrete_sequence=["#315D91"]
    )

    fig_categories.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        textfont=dict(color="#243247", size=11),
        cliponaxis=False,
        hovertemplate="%{y}<br>Requests: %{x:,.0f}<extra></extra>"
    )

    style_chart(fig_categories, 420)

    fig_categories.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=65, t=65, b=35)
    )

    fig_categories.update_xaxes(
        showgrid=True,
        gridcolor="#E8EDF2"
    )

    fig_categories.update_yaxes(
        showgrid=False
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
        title="Top Neighbourhoods",
        text="total_requests",
        color_discrete_sequence=["#0F766E"]
    )

    fig_neighbourhoods.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        textfont=dict(color="#243247", size=11),
        cliponaxis=False,
        hovertemplate="%{y}<br>Requests: %{x:,.0f}<extra></extra>"
    )

    style_chart(fig_neighbourhoods, 420)

    fig_neighbourhoods.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=65, t=65, b=35)
    )

    fig_neighbourhoods.update_xaxes(
        showgrid=True,
        gridcolor="#E8EDF2"
    )

    fig_neighbourhoods.update_yaxes(
        showgrid=False
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
    hole=0.55,
    title="Request Status Distribution",
    color_discrete_sequence=[
        "#0F766E",
        "#315D91",
        "#E6A64C",
        "#7564A8",
        "#C76B51"
    ]
)

fig_status.update_traces(
    textposition="inside",
    textinfo="percent",
    textfont=dict(
        color="#FFFFFF",
        size=12
    ),
    marker=dict(
        line=dict(color="#FFFFFF", width=2)
    ),
    hovertemplate="%{label}<br>Requests: %{value:,.0f}<br>%{percent}<extra></extra>"
)

style_chart(fig_status, 420)

fig_status.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",
        y=-0.08,
        x=0.5,
        xanchor="center"
    )
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
                context = build_analytics_context(data)
                answer = ask_ai(question, context=context)
                st.markdown(answer)

            except Exception as error:
                st.error(f"AI analysis failed: {error}")
