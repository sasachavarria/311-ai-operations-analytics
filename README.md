# Edmonton 311 AI Operations Analytics

An interactive data analytics application that combines PostgreSQL, Python, Plotly, and LLMs to explore Edmonton 311 service request data through dashboards and natural-language questions.

## Project Overview

This project analyzes Edmonton 311 service requests to identify operational trends, service demand patterns, and unusual activity.

Users can explore the data through interactive visualizations and ask natural-language questions using a locally hosted AI model (Ollama).

## Features

- **Interactive Dashboard:** Explore service requests by year, category, neighbourhood, and status.
- **PostgreSQL Integration:** Store and query structured service request data.
- **AI Analyst:** Ask questions about service request trends using natural language.
- **Data Visualization:** Interactive charts and graphs built with Plotly.
- **Operational Analysis:** Identify trends, category distributions, and potential anomalies.
- **Local AI Processing:** Use Ollama to run a language model locally.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| PostgreSQL | Database management |
| SQLAlchemy | Database connectivity |
| Pandas | Data processing |
| Streamlit | Interactive user interface |
| Plotly | Data visualization |
| Ollama | Local LLM integration |
| Git/GitHub | Version control |

## Project Structure

```text
311-ai-operations-analytics/
│
├── app.py             # Main Streamlit application
├── database.py        # PostgreSQL connectivity
├── analysis.py        # SQL queries and data analysis
├── ai_analyst.py      # Ollama integration and AI responses
├── reports.py         # Reporting and anomaly detection
├── test_app.py        # Application testing
├── requirements.txt   # Python dependencies
├── .gitignore         # Excluded files and credentials
└── README.md          # Project documentation
```

## How It Works

1. Service request data is stored in PostgreSQL.
2. Python retrieves and processes data using SQLAlchemy and Pandas.
3. Streamlit provides an interactive interface for exploring the dataset.
4. Plotly generates interactive data visualizations.
5. Ollama processes natural-language questions and generates explanations using analytical context.

## Installation

### Requirements
- Python 3.10+
- PostgreSQL
- Ollama

### Setup

Clone the repository:

```bash
git clone https://github.com/sasachavarria/311-ai-operations-analytics.git
cd 311-ai-operations-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your environment variables in a `.env` file:

```text
DATABASE_URL=your_postgresql_connection_string
```

Ensure PostgreSQL is running and the database has been populated with the required service request data.

Start Ollama and ensure the required model is available.

Run the application:

```bash
streamlit run app.py
```

## Current Limitations

- AI-generated responses may occasionally be inaccurate or incomplete.
- Large datasets require careful context management when interacting with LLMs.
- AI-generated explanations should be validated against database results.
- The application is currently designed around Edmonton 311 service request data.

## Future Improvements

- Implement controlled natural-language-to-SQL querying.
- Improve AI response validation and reliability.
- Expand analytical capabilities and anomaly detection.
- Introduce automated reporting and additional operational metrics.
- Improve scalability and database query performance.

## Motivation

This project was independently developed to explore how database technologies, data analytics, and locally hosted AI models can make operational information more accessible and actionable.

It also served as a practical opportunity to develop skills in PostgreSQL, Python, AI integration, and application development through independent learning and AI-assisted coding.