
import streamlit as st


def apply_shared_filters(movies, genres, movie_genres):

    # --------------------------------
    # INITIALIZE PERSISTENT VALUES
    # --------------------------------

    if "filter_years" not in st.session_state:
        st.session_state.filter_years = (
            int(movies["release_year"].min()),
            int(movies["release_year"].max())
        )

    if "filter_min_rating" not in st.session_state:
        st.session_state.filter_min_rating = 0.0

    if "filter_genres" not in st.session_state:
        st.session_state.filter_genres = []

    if "filter_language" not in st.session_state:
        st.session_state.filter_language = "All"

    # --------------------------------
    # RESTORE WIDGET VALUES
    # --------------------------------

    st.session_state["_year_widget"] = st.session_state.filter_years
    st.session_state["_rating_widget"] = st.session_state.filter_min_rating
    st.session_state["_genre_widget"] = st.session_state.filter_genres
    st.session_state["_language_widget"] = st.session_state.filter_language

    # --------------------------------
    # CALLBACKS
    # --------------------------------

    def save_years():
        st.session_state.filter_years = st.session_state["_year_widget"]

    def save_rating():
        st.session_state.filter_min_rating = st.session_state["_rating_widget"]

    def save_genres():
        st.session_state.filter_genres = st.session_state["_genre_widget"]

    def save_language():
        st.session_state.filter_language = st.session_state["_language_widget"]

    # --------------------------------
    # SIDEBAR FILTERS
    # --------------------------------

    st.sidebar.title("🎬 Movie Filters")

    st.sidebar.slider(
        "Select Release Year Range",
        min_value=int(movies["release_year"].min()),
        max_value=int(movies["release_year"].max()),
        key="_year_widget",
        on_change=save_years
    )

    st.sidebar.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=10.0,
        step=0.1,
        key="_rating_widget",
        on_change=save_rating
    )

    genre_options = sorted(genres["genre_name"].dropna().unique())

    st.sidebar.multiselect(
        "Select Genres",
        options=genre_options,
        key="_genre_widget",
        on_change=save_genres
    )

    language_options = sorted(
        movies["original_language"].dropna().unique()
    )

    # Keep the saved language valid
    if st.session_state.filter_language not in ["All"] + language_options:
        st.session_state.filter_language = "All"
        st.session_state["_language_widget"] = "All"

    st.sidebar.selectbox(
        "Select Language",
        options=["All"] + language_options,
        key="_language_widget",
        on_change=save_language
    )

    # --------------------------------
    # APPLY FILTERS
    # --------------------------------

    filtered_movies = movies.copy()

    years = st.session_state.filter_years

    filtered_movies = filtered_movies[
        (filtered_movies["release_year"] >= years[0]) &
        (filtered_movies["release_year"] <= years[1])
    ]

    filtered_movies = filtered_movies[
        filtered_movies["vote_average"] >=
        st.session_state.filter_min_rating
    ]

    language = st.session_state.filter_language

    if language != "All":
        filtered_movies = filtered_movies[
            filtered_movies["original_language"] == language
        ]

    selected_genres = st.session_state.filter_genres

    if selected_genres:
        selected_genre_ids = genres[
            genres["genre_name"].isin(selected_genres)
        ]["genre_id"]

        selected_movie_ids = movie_genres[
            movie_genres["genre_id"].isin(selected_genre_ids)
        ]["movie_id"].unique()

        filtered_movies = filtered_movies[
            filtered_movies["movie_id"].isin(selected_movie_ids)
        ]

    # --------------------------------
    # DISPLAY MATCHING MOVIE COUNT
    # --------------------------------

    st.sidebar.success(
        f"{filtered_movies['movie_id'].nunique():,} movies found"
    )

    return filtered_movies
