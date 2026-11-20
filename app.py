import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from common_filters import apply_shared_filters 

st.set_page_config(
    page_title="Reel Insights",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Reel Insights")
st.subheader("An End-to-End Exploratory Data Analysis of the Global Movie Industry")

DATA_PATH = "TMDB_data/cleaned/"

movies = pd.read_csv(DATA_PATH + "movies_cleaned.csv")
genres = pd.read_csv(DATA_PATH + "genres_cleaned.csv")
movie_genres = pd.read_csv(DATA_PATH + "movie_genres_cleaned.csv")
cast = pd.read_csv(DATA_PATH + "cast_cleaned.csv")
crew = pd.read_csv(DATA_PATH + "crew_cleaned.csv")
movie_keywords = pd.read_csv(DATA_PATH + "movie_keywords_cleaned.csv")

# st.success("All datasets loaded successfully!")



# st.subheader("Dataset Overview")

# st.write("Movies:", movies.shape)
# st.write("Genres:", genres.shape)
# st.write("Movie Genres:", movie_genres.shape)
# st.write("Cast:", cast.shape)
# st.write("Crew:", crew.shape)
# st.write("Movie Keywords:", movie_keywords.shape)



# --------------------------------
# INITIALIZE PERSISTENT FILTER VALUES
# --------------------------------

# if "filter_years" not in st.session_state:
#     st.session_state.filter_years = (
#         int(movies["release_year"].min()),
#         int(movies["release_year"].max())
#     )

# if "filter_min_rating" not in st.session_state:
#     st.session_state.filter_min_rating = 0.0

# if "filter_genres" not in st.session_state:
#     st.session_state.filter_genres = []

# if "filter_language" not in st.session_state:
#     st.session_state.filter_language = "All"


# --------------------------------
# CALLBACK FUNCTIONS
# --------------------------------

# def save_years():
#     st.session_state.filter_years = st.session_state._year_widget

# def save_rating():
#     st.session_state.filter_min_rating = st.session_state._rating_widget

# def save_genres():
#     st.session_state.filter_genres = st.session_state._genre_widget

# def save_language():
#     st.session_state.filter_language = st.session_state._language_widget


# --------------------------------
# RESTORE WIDGET VALUES
# --------------------------------

# if "_year_widget" not in st.session_state:
#     st.session_state._year_widget = st.session_state.filter_years

# if "_rating_widget" not in st.session_state:
#     st.session_state._rating_widget = st.session_state.filter_min_rating

# if "_genre_widget" not in st.session_state:
#     st.session_state._genre_widget = st.session_state.filter_genres

# if "_language_widget" not in st.session_state:
#     st.session_state._language_widget = st.session_state.filter_language


# --------------------------------
# SIDEBAR FILTERS
# --------------------------------

# st.sidebar.title("🎬 Movie Filters")

# st.sidebar.slider(
#     "Select Release Year Range",
#     min_value=int(movies["release_year"].min()),
#     max_value=int(movies["release_year"].max()),
#     key="_year_widget",
#     on_change=save_years
# )

# st.sidebar.slider(
#     "Minimum Rating",
#     min_value=0.0,
#     max_value=10.0,
#     step=0.1,
#     key="_rating_widget",
#     on_change=save_rating
# )

# genre_options = sorted(genres["genre_name"].dropna().unique())

# st.sidebar.multiselect(
#     "Select Genres",
#     options=genre_options,
#     key="_genre_widget",
#     on_change=save_genres
# )

# language_options = sorted(
#     movies["original_language"].dropna().unique()
# )

# st.sidebar.selectbox(
#     "Select Language",
#     options=["All"] + language_options,
#     key="_language_widget",
#     on_change=save_language
# )

# # Maintain compatibility with existing dashboard chart code
# selected_years = st.session_state.filter_years
# min_rating = st.session_state.filter_min_rating
# selected_genres = st.session_state.filter_genres
# selected_language = st.session_state.filter_language


# selected_languages = (
#     [] if selected_language == "All"
#     else [selected_language]
# )

# --------------------------------
# APPLY FILTERS
# --------------------------------

#filtered_movies = movies.copy()

# Release year
# filtered_movies = filtered_movies[
#     (filtered_movies["release_year"] >= st.session_state.filter_years[0]) &
#     (filtered_movies["release_year"] <= st.session_state.filter_years[1])
# ]

# # Minimum rating
# filtered_movies = filtered_movies[
#     filtered_movies["vote_average"] >= st.session_state.filter_min_rating
# ]

# # Language
# if st.session_state.filter_language != "All":
#     filtered_movies = filtered_movies[
#         filtered_movies["original_language"] ==
#         st.session_state.filter_language
#     ]

# Genre
# if st.session_state.filter_genres:

#     selected_genre_ids = genres[
#         genres["genre_name"].isin(st.session_state.filter_genres)
#     ]["genre_id"]

#     selected_movie_ids = movie_genres[
#         movie_genres["genre_id"].isin(selected_genre_ids)
#     ]["movie_id"].unique()

#     filtered_movies = filtered_movies[
#         filtered_movies["movie_id"].isin(selected_movie_ids)
#     ]

# # Matching movie count
# st.sidebar.success(
#     f"{filtered_movies['movie_id'].nunique():,} movies found"
# )

 # --------------------------------
# SHARED FILTERS
# --------------------------------

filtered_movies = apply_shared_filters(
    movies,
    genres,
    movie_genres
)

# Compatibility with existing dashboard chart code
selected_years = st.session_state.filter_years
min_rating = st.session_state.filter_min_rating
selected_genres = st.session_state.filter_genres
selected_language = st.session_state.filter_language

selected_languages = (
    [] if selected_language == "All"
    else [selected_language]
)




st.subheader("Movie Analytics Overview")

# Calculate metrics
total_movies = movies["movie_id"].nunique()
total_genres = genres["genre_id"].nunique()
total_actors = cast["person_id"].nunique()
total_crew = crew["person_id"].nunique()

# Create four columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
    "Total Movies",
    f"{filtered_movies['movie_id'].nunique():,}"
)

with col2:
    st.metric(
        label="Total Genres",
        value=f"{total_genres:,}"
    )

with col3:
    st.metric(
        label="Unique Actors",
        value=f"{total_actors:,}"
    )

with col4:
    st.metric(
        label="Unique Crew Members",
        value=f"{total_crew:,}"
    )


# st.divider()

# st.subheader("🏆 Top 10 Highest-Grossing Movies")

# # Remove movies with zero revenue
# valid_revenue = movies[movies["revenue"] > 0].copy()

# # Sort movies by revenue
# top_10_revenue = valid_revenue.sort_values(
#     by="revenue",
#     ascending=False
# ).head(10)

# # Convert revenue into millions
# top_10_revenue["revenue_millions"] = (
#     top_10_revenue["revenue"] / 1000000
# )


# fig = px.bar(
#     top_10_revenue.sort_values(
#         by="revenue_millions",
#         ascending=True
#     ),
#     x="revenue_millions",
#     y="title",
#     orientation="h",
#     color="revenue_millions",
#     color_continuous_scale="viridis",
#     #title="Top 10 Highest-Grossing Movies",
#     labels={
#         "revenue_millions": "Revenue (Millions USD)",
#         "title": "Movie"
#     },
#     hover_data={
#         "revenue_millions": ":.2f"
#     }
# )

# fig.update_layout(
#     height=550,
#     showlegend=False
# )

# st.plotly_chart(fig, use_container_width=True)



# --------------------------------
# TOP 10 HIGHEST-GROSSING MOVIES
# --------------------------------

st.divider()

st.subheader("🏆 Top 10 Highest-Grossing Movies")

# Filter movies with valid revenue
top_grossing = filtered_movies[
    filtered_movies["revenue"] > 0
].copy()

# Select top 10 movies by revenue
top_grossing = top_grossing.nlargest(
    10, "revenue"
)

# Convert revenue into millions for display
top_grossing["revenue_millions"] = (
    top_grossing["revenue"] / 1_000_000
)

# Sort for horizontal bar chart
top_grossing = top_grossing.sort_values(
    by="revenue_millions",
    ascending=True
)

# Create Plotly chart
fig_revenue = px.bar(
    top_grossing,
    x="revenue_millions",
    y="title",
    orientation="h",
    color="revenue_millions",
    color_continuous_scale="Viridis",
    labels={
        "revenue_millions": "Revenue (Millions USD)",
        "title": "Movie"
    },
    #title="Top 10 Highest-Grossing Movies"
)

fig_revenue.update_layout(
    height=550,
    showlegend=False,
    yaxis_title="Movie",
    xaxis_title="Revenue (Millions USD)"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)



# st.divider()

# st.subheader("🎭 Movie Distribution by Genre")

# # Merge movie_genres with genres
# genre_data = movie_genres.merge(
#     genres,
#     on="genre_id",
#     how="left"
# )

# # Count unique movies in each genre
# genre_counts = (
#     genre_data.groupby("genre_name")["movie_id"]
#     .nunique()
#     .reset_index(name="total_movies")
# )

# # Sort by movie count
# genre_counts = genre_counts.sort_values(
#     by="total_movies",
#     ascending=True
# )


# fig_genre = px.bar(
#     genre_counts,
#     x="total_movies",
#     y="genre_name",
#     orientation="h",
#     color_discrete_sequence=["#10B981"],
#     labels={
#         "total_movies": "Number of Movies",
#         "genre_name": "Genre"
#     }
# )

# fig_genre.update_layout(
#     height=650,
#     showlegend=False,
#     title="Number of Movies by Genre"
# )

# st.plotly_chart(
#     fig_genre,
#     use_container_width=True
# )

# --------------------------------
# NUMBER OF MOVIES BY GENRE
# --------------------------------

st.divider()

st.subheader("🎭 Number of Movies by Genre")

# Get genre records belonging to filtered movies
filtered_movie_genres = movie_genres[
    movie_genres["movie_id"].isin(
        filtered_movies["movie_id"]
    )
]

# Join with genre names
genre_data = filtered_movie_genres.merge(
    genres,
    on="genre_id",
    how="left"
)

# Count unique movies in each genre
genre_counts = (
    genre_data.groupby("genre_name")["movie_id"]
    .nunique()
    .reset_index(name="total_movies")
    .sort_values("total_movies", ascending=True)
)

# Create horizontal bar chart
fig_genre = px.bar(
    genre_counts,
    x="total_movies",
    y="genre_name",
    orientation="h",
    color_discrete_sequence=["#00CC96"],
    labels={
        "total_movies": "Number of Movies",
        "genre_name": "Genre"
    },
    #title="Number of Movies by Genre"
)

fig_genre.update_layout(
    height=650,
    showlegend=False
)

st.plotly_chart(
    fig_genre,
    use_container_width=True
)


# st.divider()

# st.subheader("💰 Movie Budget vs Revenue")

# budget_revenue_data = movie_genres.merge(
#     genres,
#     on="genre_id",
#     how="left"
# )

# budget_revenue_data = budget_revenue_data.merge(
#     movies[
#         ["movie_id", "budget", "revenue", "title"]
#     ],
#     on="movie_id",
#     how="left"
# )

# budget_revenue_data = budget_revenue_data[
#     (budget_revenue_data["budget"] > 0) &
#     (budget_revenue_data["revenue"] > 0)
# ].copy()


# # Get each movie's primary genre
# primary_genre_data = movie_genres.merge(
#     genres,
#     on="genre_id",
#     how="left"
# )

# primary_genre_data = (
#     primary_genre_data
#     .drop_duplicates(subset="movie_id", keep="first")
# )

# budget_revenue_data = movies[
#     ["movie_id", "title", "budget", "revenue"]
# ].merge(
#     primary_genre_data[["movie_id", "genre_name"]],
#     on="movie_id",
#     how="inner"
# )

# budget_revenue_data = budget_revenue_data[
#     (budget_revenue_data["budget"] > 0) &
#     (budget_revenue_data["revenue"] > 0)
# ].copy()

# budget_revenue_data["budget_millions"] = (
#     budget_revenue_data["budget"] / 1000000
# )

# budget_revenue_data["revenue_millions"] = (
#     budget_revenue_data["revenue"] / 1000000
# )

# fig_budget = px.scatter(
#     budget_revenue_data,
#     x="budget_millions",
#     y="revenue_millions",
#     color="genre_name",
#     hover_name="title",
#     title="Movie Budget vs Revenue by Primary Genre",
#     labels={
#         "budget_millions": "Budget (Millions USD)",
#         "revenue_millions": "Revenue (Millions USD)",
#         "genre_name": "Primary Genre"
#     }
# )

# fig_budget.update_layout(height=650)
# # fig_budget.update_traces(
# #     marker=dict(
# #         size=9,
# #         opacity=0.6
# #     )
# # )
# st.plotly_chart(
#     fig_budget,
#     use_container_width=True
# )

# --------------------------------
# BUDGET VS REVENUE BY PRIMARY GENRE
# --------------------------------

st.divider()

st.subheader("💰 Movie Budget vs Revenue by Primary Genre")

# Identify the first genre listed for each movie
primary_genres = movie_genres.copy()

primary_genres["genre_order"] = (
    primary_genres.groupby("movie_id").cumcount()
)

primary_genres = primary_genres[
    primary_genres["genre_order"] == 0
]

# Attach genre names
primary_genres = primary_genres.merge(
    genres,
    on="genre_id",
    how="left"
)

# Rename genre column
primary_genres = primary_genres[
    ["movie_id", "genre_name"]
].rename(
    columns={"genre_name": "primary_genre"}
)

# Merge with filtered movies
budget_revenue_data = filtered_movies.merge(
    primary_genres,
    on="movie_id",
    how="left"
)

# Keep valid budget and revenue values
budget_revenue_data = budget_revenue_data[
    (budget_revenue_data["budget"] > 0) &
    (budget_revenue_data["revenue"] > 0)
].copy()

# Convert USD to millions
budget_revenue_data["budget_millions"] = (
    budget_revenue_data["budget"] / 1_000_000
)

budget_revenue_data["revenue_millions"] = (
    budget_revenue_data["revenue"] / 1_000_000
)



fig_budget = px.scatter(
    budget_revenue_data,
    x="budget_millions",
    y="revenue_millions",
    color="primary_genre",
    size="vote_count",
    hover_name="title",
    hover_data={
        "budget_millions": ":.2f",
        "revenue_millions": ":.2f",
        "vote_count": True,
        "primary_genre": True
    },
    size_max=25,
    opacity=0.65,
    labels={
        "budget_millions": "Budget (Millions USD)",
        "revenue_millions": "Revenue (Millions USD)",
        "primary_genre": "Primary Genre",
        "vote_count": "Vote Count"
    },
    #title="Movie Budget vs Revenue by Primary Genre"
)

fig_budget.update_layout(height=650)

st.plotly_chart(
    fig_budget,
    use_container_width=True
)





# st.divider()

# st.subheader("⭐ Average Movie Rating by Genre")

# rating_genre_data = movie_genres.merge(
#     genres,
#     on="genre_id",
#     how="left"
# )

# rating_genre_data = rating_genre_data.merge(
#     movies[["movie_id", "vote_average"]],
#     on="movie_id",
#     how="left"
# )

# rating_genre_data = rating_genre_data.dropna(
#     subset=["vote_average"]
# )

# genre_ratings = (
#     rating_genre_data.groupby("genre_name")["vote_average"]
#     .mean()
#     .reset_index(name="average_rating")
# )

# genre_ratings = genre_ratings.sort_values(
#     by="average_rating",
#     ascending=True
# )


# fig_rating = px.bar(
#     genre_ratings,
#     x="average_rating",
#     y="genre_name",
#     orientation="h",
#     color="average_rating",
#     color_continuous_scale="Viridis",
#     labels={
#         "average_rating": "Average Rating",
#         "genre_name": "Genre"
#     },
    
# )

# fig_rating.update_layout(
#     height=600,
#     coloraxis_showscale=False
# )

# st.plotly_chart(
#     fig_rating,
#     use_container_width=True
# )

# --------------------------------
# AVERAGE MOVIE RATING BY GENRE
# --------------------------------

st.divider()

st.subheader("⭐ Average Movie Rating by Genre")

# Get genres for filtered movies
rating_genres = movie_genres[
    movie_genres["movie_id"].isin(
        filtered_movies["movie_id"]
    )
]
if selected_genres:
    selected_genre_ids = genres[
        genres["genre_name"].isin(selected_genres)
    ]["genre_id"]

    rating_genres = rating_genres[
        rating_genres["genre_id"].isin(selected_genre_ids)
    ]
# Merge movie ratings with genres
rating_data = rating_genres.merge(
    filtered_movies[["movie_id", "vote_average"]],
    on="movie_id",
    how="inner"
).merge(
    genres,
    on="genre_id",
    how="left"
)

# Calculate average rating per genre
genre_ratings = (
    rating_data.groupby("genre_name")["vote_average"]
    .mean()
    .reset_index(name="average_rating")
    .sort_values("average_rating", ascending=True)
)

fig_rating = px.bar(
    genre_ratings,
    x="average_rating",
    y="genre_name",
    orientation="h",
    color="average_rating",
    color_continuous_scale="Viridis",
    labels={
        "average_rating": "Average Rating",
        "genre_name": "Genre"
    },
    #title="Average Movie Rating by Genre"
)

fig_rating.update_layout(
    height=650,
    xaxis_range=[0, 10]
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)




# st.divider()

# st.subheader("📅 Movie Releases Over the Years")

# yearly_movies = (
#     filtered_movies.groupby("release_year")["movie_id"]
#     .nunique()
#     .reset_index(name="total_movies")
#     .sort_values("release_year")
# )

# fig_year = px.line(
#     yearly_movies,
#     x="release_year",
#     y="total_movies",
#     markers=True,
#     labels={
#         "release_year": "Release Year",
#         "total_movies": "Number of Movies"
#     },
#     #title="Number of Movies Released Per Year"
# )

# fig_year.update_traces(
#     line=dict(color="#00CC96", width=3),
#     marker=dict(size=6)
# )

# fig_year.update_layout(height=500)

# st.plotly_chart(
#     fig_year,
#     use_container_width=True
# )

# --------------------------------
# MOVIE RELEASES OVER THE YEARS
# --------------------------------

st.divider()

st.subheader("📅 Movie Releases Over the Years")

yearly_movies = (
    filtered_movies.groupby("release_year")["movie_id"]
    .nunique()
    .reset_index(name="total_movies")
    .sort_values("release_year")
)

fig_year = px.line(
    yearly_movies,
    x="release_year",
    y="total_movies",
    markers=True,
    labels={
        "release_year": "Release Year",
        "total_movies": "Number of Movies"
    }
)

fig_year.update_traces(
    line=dict(color="#00CC96", width=3),
    marker=dict(size=6)
)

fig_year.update_layout(height=500)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# st.divider()

# st.subheader("🎭 Top 10 Actors by Movie Count")

# actor_movies = (
#     cast.groupby(["person_id", "actor_name"])["movie_id"]
#     .nunique()
#     .reset_index(name="total_movies")
# )

# top_actors = actor_movies.sort_values(
#     by="total_movies",
#     ascending=False
# ).head(10)


# fig_actors = px.bar(
#     top_actors.sort_values("total_movies", ascending=True),
#     x="total_movies",
#     y="actor_name",
#     orientation="h",
#     color_discrete_sequence=["#AB63FA"],
#     labels={
#         "total_movies": "Number of Movies",
#         "actor_name": "Actor"
#     },
#     #title="Top 10 Most Prolific Actors"
# )

# fig_actors.update_layout(
#     height=550,
#     showlegend=False
# )

# st.plotly_chart(
#     fig_actors,
#     use_container_width=True
# )

# --------------------------------
# TOP 10 ACTORS BY MOVIE COUNT
# --------------------------------

st.divider()

st.subheader("🎭 Top 10 Actors by Movie Count")

# Get cast records for filtered movies
filtered_cast = cast[
    cast["movie_id"].isin(
        filtered_movies["movie_id"]
    )
].copy()

# Count unique movies for each actor
actor_movies = (
    filtered_cast.groupby(
        ["person_id", "actor_name"]
    )["movie_id"]
    .nunique()
    .reset_index(name="total_movies")
)

# Select top 10 actors
top_actors = actor_movies.nlargest(
    10, "total_movies"
)

# Sort for horizontal bar chart
top_actors = top_actors.sort_values(
    "total_movies",
    ascending=True
)

# Create chart
fig_actors = px.bar(
    top_actors,
    x="total_movies",
    y="actor_name",
    orientation="h",
    color_discrete_sequence=["#AB63FA"],
    labels={
        "total_movies": "Number of Movies",
        "actor_name": "Actor"
    },
    title="Top 10 Actors by Movie Count"
)

fig_actors.update_layout(
    height=550,
    showlegend=False
)

st.plotly_chart(
    fig_actors,
    use_container_width=True
)


# st.divider()

# st.subheader("🎬 Top 10 Directors by Movie Count")

# director_movies = crew[
#     crew["job"] == "Director"
# ].copy()

# director_counts = (
#     director_movies.groupby(
#         ["person_id", "person_name"]
#     )["movie_id"]
#     .nunique()
#     .reset_index(name="total_movies")
# )

# top_directors = director_counts.sort_values(
#     by="total_movies",
#     ascending=False
# ).head(10)


# fig_directors = px.bar(
#     top_directors.sort_values(
#         "total_movies",
#         ascending=True
#     ),
#     x="total_movies",
#     y="person_name",
#     orientation="h",
#     color_discrete_sequence=["#F59E0B"],
#     labels={
#         "total_movies": "Number of Movies",
#         "person_name": "Director"
#     },
#     #title="Top 10 Directors by Movie Count"
# )

# fig_directors.update_layout(
#     height=550,
#     showlegend=False
# )

# st.plotly_chart(
#     fig_directors,
#     use_container_width=True
# )

# --------------------------------
# TOP 10 DIRECTORS BY MOVIE COUNT
# --------------------------------

st.divider()

st.subheader("🎬 Top 10 Directors by Movie Count")

# Get crew records for filtered movies
filtered_crew = crew[
    (crew["movie_id"].isin(filtered_movies["movie_id"])) &
    (crew["job"] == "Director")
].copy()

# Count unique movies directed by each director
director_counts = (
    filtered_crew.groupby(
        ["person_id", "person_name"]
    )["movie_id"]
    .nunique()
    .reset_index(name="total_movies")
)

# Select top 10 directors
top_directors = director_counts.nlargest(
    10, "total_movies"
)

# Sort for horizontal bar chart
top_directors = top_directors.sort_values(
    "total_movies",
    ascending=True
)

# Create Plotly chart
fig_directors = px.bar(
    top_directors,
    x="total_movies",
    y="person_name",
    orientation="h",
    color_discrete_sequence=["#F59E0B"],
    labels={
        "total_movies": "Number of Movies",
        "person_name": "Director"
    },
    title="Top 10 Directors by Movie Count"
)

fig_directors.update_layout(
    height=550,
    showlegend=False
)

st.plotly_chart(
    fig_directors,
    use_container_width=True
)



