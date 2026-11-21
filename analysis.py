import pandas as pd
from sqlalchemy import text
from database import read_data, engine


def get_overview():
    query = """
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT row_id) AS unique_ids,
        SUM(count) AS total_requests,
        COUNT(DISTINCT service_category) AS total_categories,
        COUNT(DISTINCT neighbourhood) AS total_neighbourhoods,
        MIN(date_created) AS first_request,
        MAX(date_created) AS latest_request
    FROM service_requests;
    """
    return read_data(query)


def get_top_categories(limit=10):
    query = f"""
    SELECT service_category, SUM(count) AS total_requests
    FROM service_requests
    WHERE service_category IS NOT NULL
    GROUP BY service_category
    ORDER BY total_requests DESC
    LIMIT {int(limit)};
    """
    return read_data(query)


def get_monthly_trends():
    query = """
    SELECT year, month_number, month, SUM(count) AS total_requests
    FROM service_requests
    GROUP BY year, month_number, month
    ORDER BY year, month_number;
    """
    return read_data(query)


def get_top_neighbourhoods(limit=10):
    query = f"""
    SELECT neighbourhood, SUM(count) AS total_requests
    FROM service_requests
    WHERE neighbourhood IS NOT NULL
    GROUP BY neighbourhood
    ORDER BY total_requests DESC
    LIMIT {int(limit)};
    """
    return read_data(query)


def get_status_breakdown():
    query = """
    SELECT request_status, SUM(count) AS total_requests
    FROM service_requests
    WHERE request_status IS NOT NULL
    GROUP BY request_status
    ORDER BY total_requests DESC;
    """
    return read_data(query)


def get_service_areas():
    query = """
    SELECT service_area, SUM(count) AS total_requests
    FROM service_requests
    WHERE service_area IS NOT NULL
    GROUP BY service_area
    ORDER BY total_requests DESC;
    """
    return read_data(query)


def get_filter_options():
    years = read_data("""
        SELECT DISTINCT year FROM service_requests
        WHERE year IS NOT NULL ORDER BY year;
    """)

    categories = read_data("""
        SELECT DISTINCT service_category FROM service_requests
        WHERE service_category IS NOT NULL ORDER BY service_category;
    """)

    neighbourhoods = read_data("""
        SELECT DISTINCT neighbourhood FROM service_requests
        WHERE neighbourhood IS NOT NULL ORDER BY neighbourhood;
    """)

    return (
        years["year"].tolist(),
        categories["service_category"].tolist(),
        neighbourhoods["neighbourhood"].tolist()
    )


def get_filtered_data(years=None, categories=None, neighbourhoods=None):
    query = """
        SELECT
            year,
            month,
            month_number,
            service_category,
            neighbourhood,
            request_status,
            SUM(count) AS total_requests
        FROM service_requests
        WHERE 1=1
    """

    params = {}

    if years:
        query += " AND year IN :years"
        params["years"] = [int(y) for y in years]

    if categories:
        query += " AND service_category IN :categories"
        params["categories"] = categories

    if neighbourhoods:
        query += " AND neighbourhood IN :neighbourhoods"
        params["neighbourhoods"] = neighbourhoods

    query += """
        GROUP BY
            year, month, month_number,
            service_category, neighbourhood, request_status
        ORDER BY year, month_number;
    """

    statement = text(query)

    if years:
        from sqlalchemy import bindparam
        statement = statement.bindparams(bindparam("years", expanding=True))

    if categories:
        from sqlalchemy import bindparam
        statement = statement.bindparams(bindparam("categories", expanding=True))

    if neighbourhoods:
        from sqlalchemy import bindparam
        statement = statement.bindparams(bindparam("neighbourhoods", expanding=True))

    with engine.connect() as connection:
        return pd.read_sql_query(statement, connection, params=params)
