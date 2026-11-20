
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

from common_filters import apply_shared_filters


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Query Explorer | Reel Insights",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Query Explorer")
st.write("Explore all 10 SQL questions from the TMDB movie analysis project.")


# ==================================================
# LOAD DATA FOR SHARED FILTER CONTROLS
# ==================================================

DATA_PATH = "TMDB_data/cleaned/"

movies = pd.read_csv(DATA_PATH + "movies_cleaned.csv")
genres = pd.read_csv(DATA_PATH + "genres_cleaned.csv")
movie_genres = pd.read_csv(DATA_PATH + "movie_genres_cleaned.csv")


# ==================================================
# SHARED FILTERS
# ==================================================

filtered_movies = apply_shared_filters(
    movies,
    genres,
    movie_genres
)

# Get the selected movie IDs for SQL filtering
filtered_movie_ids = filtered_movies["movie_id"].dropna().unique().tolist()


# ==================================================
# MYSQL CONNECTION
# ==================================================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reel_insights"
    )


# ==================================================
# SQL EXECUTION FUNCTION
# ==================================================

def run_query(query, params=None):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        return pd.DataFrame(rows, columns=columns)

    finally:
        cursor.close()
        connection.close()


# ==================================================
# FILTERED MOVIE SQL CONDITIONS
# ==================================================

def get_filtered_movie_condition():

    if not filtered_movie_ids:
        return "1 = 0", []

    placeholders = ", ".join(["%s"] * len(filtered_movie_ids))

    return f"m.movie_id IN ({placeholders})", filtered_movie_ids


movie_condition, movie_params = get_filtered_movie_condition()


# ==================================================
# SAVED SQL QUESTIONS
# ==================================================

query_options = {
    "Q1 - Action Movies Released After 2015": 1,
    "Q2 - Top 10 Highest-Grossing Movies": 2,
    "Q3 - Average Budget and Revenue by Genre": 3,
    "Q4 - Top 10 Actors by Movie Count": 4,
    "Q5 - Directors with More Than 3 Movies": 5,
    "Q6 - Top 10 Most Used Keywords": 6,
    "Q7 - Budget Above Average and Revenue Below Average": 7,
    "Q8 - Actors in Christopher Nolan Movies": 8,
    "Q9 - Highest Average Rating by Genre": 9,
    "Q10 - Top 10 Movies by Keyword Count": 10
}

selected_query = st.selectbox(
    "Select a SQL Question",
    list(query_options.keys())
)

query_number = query_options[selected_query]

st.divider()


# ==================================================
# EXECUTE SELECTED QUERY
# ==================================================

try:

    
# --------------------------------------------------
# Q1: ACTION MOVIES AFTER 2015
# Using cleaned CSV data
# --------------------------------------------------

    if query_number == 1:

        # Get selected Action genre
        action_genre_ids = genres[
            genres["genre_name"] == "Action"
        ]["genre_id"]

        action_movie_ids = movie_genres[
            movie_genres["genre_id"].isin(action_genre_ids)
        ]["movie_id"].unique()

        # Apply all shared filters and Action genre
        result = filtered_movies[
            (filtered_movies["movie_id"].isin(action_movie_ids)) &
            (filtered_movies["release_year"] > 2015)
        ][["title", "release_date", "release_year"]].copy()

        result = result.sort_values("release_date")

        st.subheader("Action Movies Released After 2015")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            chart_data = (
                result.groupby("release_year")
                .size()
                .reset_index(name="movie_count")
            )

            fig = px.bar(
                chart_data,
                x="release_year",
                y="movie_count",
                title="Action Movies Released After 2015",
                labels={
                    "release_year": "Release Year",
                    "movie_count": "Number of Movies"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            st.info(
                f"**Insight:** {len(result)} Action movies released "
                "after 2015 match the selected filters."
            )

        else:
            st.warning("No Action movies match the selected filters.")



    # --------------------------------------------------
    # Q2: TOP 10 HIGHEST-GROSSING MOVIES
    # --------------------------------------------------

    elif query_number == 2:

        sql = f"""
        SELECT
            m.title,
            m.revenue,
            GROUP_CONCAT(
                DISTINCT g.genre_name
                ORDER BY g.genre_name
                SEPARATOR ', '
            ) AS genres
        FROM movies m
        LEFT JOIN movie_genres mg
            ON m.movie_id = mg.movie_id
        LEFT JOIN genres g
            ON mg.genre_id = g.genre_id
        WHERE {movie_condition}
        GROUP BY m.movie_id, m.title, m.revenue
        ORDER BY m.revenue DESC
        LIMIT 10;
        """

        result = run_query(sql, movie_params)

        st.subheader("Top 10 Highest-Grossing Movies")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result.sort_values("revenue"),
                x="revenue",
                y="title",
                orientation="h",
                title="Top 10 Movies by Revenue",
                labels={
                    "revenue": "Revenue ($)",
                    "title": "Movie"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            top_movie = result.iloc[0]

            st.info(
                f"**Insight:** {top_movie['title']} is the "
                f"highest-grossing movie in the filtered results."
            )


    # --------------------------------------------------
    # Q3: AVERAGE BUDGET AND REVENUE BY GENRE
    # --------------------------------------------------

    elif query_number == 3:

        sql = f"""
        SELECT
            g.genre_name,
            ROUND(AVG(m.budget), 2) AS average_budget,
            ROUND(AVG(m.revenue), 2) AS average_revenue
        FROM movies m
        INNER JOIN movie_genres mg
            ON m.movie_id = mg.movie_id
        INNER JOIN genres g
            ON mg.genre_id = g.genre_id
        WHERE {movie_condition}
        GROUP BY g.genre_id, g.genre_name
        ORDER BY average_revenue DESC;
        """

        result = run_query(sql, movie_params)

        st.subheader("Average Budget and Revenue by Genre")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result,
                x="genre_name",
                y="average_revenue",
                title="Average Revenue by Genre",
                labels={
                    "genre_name": "Genre",
                    "average_revenue": "Average Revenue ($)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            best_genre = result.iloc[0]

            st.info(
                f"**Insight:** {best_genre['genre_name']} has the "
                "highest average revenue among the filtered genres."
            )


    # --------------------------------------------------
    # Q4: TOP 10 ACTORS
    # --------------------------------------------------

    elif query_number == 4:

        sql = f"""
        SELECT
            c.actor_name,
            COUNT(DISTINCT c.movie_id) AS total_movies
        FROM `cast` c
        WHERE c.movie_id IN (
            SELECT m.movie_id
            FROM movies m
            WHERE {movie_condition}
        )
        GROUP BY c.person_id, c.actor_name
        ORDER BY total_movies DESC
        LIMIT 10;
        """

        result = run_query(sql, movie_params)

        st.subheader("Top 10 Actors by Movie Count")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result.sort_values("total_movies"),
                x="total_movies",
                y="actor_name",
                orientation="h",
                title="Top 10 Actors",
                labels={
                    "total_movies": "Number of Movies",
                    "actor_name": "Actor"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            top_actor = result.iloc[0]

            st.info(
                f"**Insight:** {top_actor['actor_name']} has appeared "
                f"in {top_actor['total_movies']} movies in the filtered results."
            )


    # --------------------------------------------------
    # Q5: DIRECTORS WITH MORE THAN 3 MOVIES
    # --------------------------------------------------

    elif query_number == 5:

        sql = f"""
        SELECT
            c.person_name AS director_name,
            COUNT(DISTINCT c.movie_id) AS total_movies
        FROM crew c
        WHERE c.job = 'Director'
          AND c.movie_id IN (
              SELECT m.movie_id
              FROM movies m
              WHERE {movie_condition}
          )
        GROUP BY c.person_id, c.person_name
        HAVING COUNT(DISTINCT c.movie_id) > 3
        ORDER BY total_movies DESC;
        """

        result = run_query(sql, movie_params)

        st.subheader("Directors with More Than 3 Movies")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result.head(10).sort_values("total_movies"),
                x="total_movies",
                y="director_name",
                orientation="h",
                title="Directors with More Than 3 Movies",
                labels={
                    "total_movies": "Number of Movies",
                    "director_name": "Director"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            st.info(
                f"**Insight:** {len(result)} directors have directed "
                "more than 3 movies in the filtered results."
            )


    # --------------------------------------------------
    # Q6: TOP 10 MOST FREQUENTLY USED KEYWORDS
    # --------------------------------------------------

    elif query_number == 6:

        sql = f"""
        SELECT
            mk.keyword_name,
            COUNT(DISTINCT mk.movie_id) AS usage_count
        FROM movie_keywords mk
        WHERE mk.movie_id IN (
            SELECT m.movie_id
            FROM movies m
            WHERE {movie_condition}
        )
        GROUP BY mk.keyword_id, mk.keyword_name
        ORDER BY usage_count DESC
        LIMIT 10;
        """

        result = run_query(sql, movie_params)

        st.subheader("Top 10 Most Frequently Used Keywords")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result.sort_values("usage_count"),
                x="usage_count",
                y="keyword_name",
                orientation="h",
                title="Top 10 Movie Keywords",
                labels={
                    "usage_count": "Number of Movies",
                    "keyword_name": "Keyword"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            top_keyword = result.iloc[0]

            st.info(
                f"**Insight:** '{top_keyword['keyword_name']}' is the "
                "most frequently used keyword in the filtered results."
            )


    # --------------------------------------------------
    # Q7: ABOVE AVERAGE BUDGET, BELOW AVERAGE REVENUE
    # --------------------------------------------------

    elif query_number == 7:

        sql = f"""
        SELECT
            m.title,
            m.budget,
            m.revenue
        FROM movies m
        WHERE {movie_condition}
          AND m.budget > (
              SELECT AVG(budget)
              FROM movies
              WHERE budget > 0
          )
          AND m.revenue < (
              SELECT AVG(revenue)
              FROM movies
              WHERE revenue > 0
          )
        ORDER BY m.budget DESC;
        """

        result = run_query(sql, movie_params)

        st.subheader(
            "Movies with Above-Average Budget and Below-Average Revenue"
        )

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.scatter(
                result,
                x="budget",
                y="revenue",
                hover_name="title",
                title="Budget vs Revenue of Selected Movies",
                labels={
                    "budget": "Budget ($)",
                    "revenue": "Revenue ($)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            st.info(
                f"**Insight:** {len(result)} movies have budgets above "
                "the overall average but revenues below the overall average."
            )


    # --------------------------------------------------
    # Q8: ACTORS IN CHRISTOPHER NOLAN MOVIES
    # --------------------------------------------------

    elif query_number == 8:

        sql = f"""
        SELECT DISTINCT
            c.actor_name
        FROM `cast` c
        INNER JOIN crew cr
            ON c.movie_id = cr.movie_id
        WHERE cr.job = 'Director'
          AND cr.person_name = 'Christopher Nolan'
          AND c.movie_id IN (
              SELECT m.movie_id
              FROM movies m
              WHERE {movie_condition}
          )
        ORDER BY c.actor_name;
        """

        result = run_query(sql, movie_params)

        st.subheader("Actors in Christopher Nolan Movies")

        st.dataframe(result, use_container_width=True)

        st.metric("Total Unique Actors", len(result))

        if not result.empty:

            st.info(
                f"**Insight:** {len(result)} unique actors appeared "
                "in Christopher Nolan movies within the filtered results."
            )


    # --------------------------------------------------
    # Q9: HIGHEST AVERAGE RATING BY GENRE
    # --------------------------------------------------

    elif query_number == 9:

        sql = f"""
        SELECT
            g.genre_name,
            ROUND(AVG(m.vote_average), 2) AS average_rating,
            COUNT(DISTINCT m.movie_id) AS total_movies
        FROM movies m
        INNER JOIN movie_genres mg
            ON m.movie_id = mg.movie_id
        INNER JOIN genres g
            ON mg.genre_id = g.genre_id
        WHERE {movie_condition}
        GROUP BY g.genre_id, g.genre_name
        HAVING COUNT(DISTINCT m.movie_id) >= 20
        ORDER BY average_rating DESC;
        """

        result = run_query(sql, movie_params)

        st.subheader("Highest Average Rating by Genre")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result.sort_values("average_rating"),
                x="average_rating",
                y="genre_name",
                orientation="h",
                title="Average Rating by Genre",
                labels={
                    "average_rating": "Average Rating",
                    "genre_name": "Genre"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            best_genre = result.iloc[0]

            st.info(
                f"**Insight:** {best_genre['genre_name']} has the "
                f"highest average rating of {best_genre['average_rating']} "
                "among genres with at least 20 filtered movies."
            )


    # --------------------------------------------------
    # Q10: TOP 10 MOVIES BY KEYWORD COUNT
    # --------------------------------------------------

    elif query_number == 10:

        sql = f"""
        SELECT
            m.title,
            COUNT(mk.keyword_id) AS keyword_count
        FROM movies m
        INNER JOIN movie_keywords mk
            ON m.movie_id = mk.movie_id
        WHERE {movie_condition}
        GROUP BY m.movie_id, m.title
        ORDER BY keyword_count DESC
        LIMIT 10;
        """

        result = run_query(sql, movie_params)

        st.subheader("Top 10 Movies by Keyword Count")

        st.dataframe(result, use_container_width=True)

        if not result.empty:

            fig = px.bar(
                result.sort_values("keyword_count"),
                x="keyword_count",
                y="title",
                orientation="h",
                title="Top 10 Movies by Number of Keywords",
                labels={
                    "keyword_count": "Number of Keywords",
                    "title": "Movie"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            top_movie = result.iloc[0]

            st.info(
                f"**Insight:** {top_movie['title']} has the highest "
                f"number of keywords ({top_movie['keyword_count']}) "
                "among the filtered movies."
            )


except mysql.connector.Error as e:

    st.error(f"MySQL Error: {e}")

except Exception as e:

    st.error(f"An error occurred: {e}")
