
import streamlit as st
import plotly.express as px
import pandas as pd

st.title("My Edmonton 311 Dashboard")

st.write("If you can see this, Streamlit is working!")

data = pd.DataFrame({
    "Month": ["January", "February", "March", "April", "May"],
    "Requests": [120, 150, 130, 190, 210]
})

fig = px.line(
    data,
    x="Month",
    y="Requests",
    markers=True,
    title="Test Monthly Requests"
)

st.plotly_chart(fig, use_container_width=True)

st.success("Plotly is working correctly!")
