# 🎬 Reel Insights: An End-to-End Exploratory Data Analysis of the Global Movie Industry (TMDB)

## 1. Project Overview

**Reel Insights** is an end-to-end data analytics project focused on exploring the global movie industry using TMDB (The Movie Database) datasets.

The project involves data cleaning, SQL analysis, Pandas-based exploratory data analysis (EDA), data visualization, and interactive dashboard development using Streamlit.

The main objective is to transform raw movie datasets into meaningful insights about movie performance, revenue, budgets, ratings, genres, actors, directors, keywords, and movie industry trends.

An interactive Streamlit application was developed to allow users to explore movie analytics through filters, dashboards, and SQL-based queries.

---

## 2. Project Objectives

- Clean and preprocess raw TMDB datasets.
- Identify and handle duplicate records and data quality issues.
- Perform relational data analysis using MySQL.
- Conduct exploratory data analysis using Pandas and NumPy.
- Calculate movie profit and Return on Investment (ROI).
- Analyze movie ratings, popularity, genres, actors, and directors.
- Identify trends in movie releases and financial performance.
- Create meaningful data visualizations.
- Develop an interactive Streamlit movie analytics application.
- Generate business insights and recommendations from the analysis.

---

## 3. Technologies Used

| Technology             | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| Python                 | Data analysis and application development |
| Pandas                 | Data cleaning, manipulation, and analysis |
| NumPy                  | Numerical operations                      |
| MySQL                  | Relational database and SQL analysis      |
| mysql-connector-python | Python-to-MySQL database connectivity     |
| Matplotlib             | Data visualization                        |
| Seaborn                | Statistical data visualization            |
| Plotly                 | Interactive charts                        |
| Streamlit              | Interactive analytics application         |
| Jupyter Notebook       | Data exploration and documentation        |

---

## 4. Dataset Description

The project uses six relational TMDB CSV datasets.

| Dataset        | Description                                                                  |
| -------------- | ---------------------------------------------------------------------------- |
| movies         | Movie information, release dates, budgets, revenues, popularity, and ratings |
| genres         | Available movie genres                                                       |
| movie_genres   | Relationship between movies and genres                                       |
| cast           | Actor and character information                                              |
| crew           | Directors and other crew information                                         |
| movie_keywords | Keywords associated with movies                                              |

### Cleaned Dataset Summary

The following six datasets were cleaned and prepared for analysis.

| Dataset        | Cleaned Rows |
| -------------- | -----------: |
| Movies         |        2,503 |
| Genres         |           19 |
| Movie Genres   |        6,878 |
| Cast           |       24,902 |
| Crew           |        7,289 |
| Movie Keywords |       41,681 |
| **Total**      |   **93,272** |

### Data Cleaning Activities

- Identified and removed exact duplicate records.
- Checked missing and zero values.
- Examined missing actor character names.
- Validated movie and genre relationships.
- Checked for orphan movie IDs and genre IDs.
- Identified invalid financial values.
- Prepared cleaned CSV files for further analysis.

---

## 5. Project Workflow

The project follows an end-to-end data analytics workflow.

### Phase 1: Data Cleaning

**Notebook:** `01_data_cleaning.ipynb`

Activities performed:

- Loaded all six TMDB datasets using Pandas.
- Inspected dataset shapes, columns, and data types.
- Checked missing values and duplicate records.
- Removed exact duplicate records.
- Validated relational data integrity.
- Examined budget and revenue values.
- Exported cleaned datasets.

### Phase 2: SQL Analysis

**Notebook:** `02_sql_analysis.ipynb`

Performed 10 SQL analysis questions using MySQL.

The analysis covered:

1. Action movies released after 2015.
2. Top 10 highest-grossing movies with their genres.
3. Average budget and revenue by genre.
4. Top 10 actors by movie count.
5. Directors who directed more than three movies.
6. Top 10 most frequently used keywords.
7. Movies with above-average budgets and below-average revenues.
8. Actors who appeared in Christopher Nolan movies.
9. Genre with the highest average rating, considering genres with at least 20 movies.
10. Top 10 movies with the highest number of keywords.

### Phase 3: Pandas Analysis

**Notebook:** `03_pandas_analysis.ipynb`

Performed 10 analytical questions using Pandas.

The analysis covered:

- Missing and zero budget/revenue values.
- Movie profit and ROI calculations.
- Top 15 ROI movies with a minimum budget threshold.
- Movie releases by year.
- Runtime statistical outliers.
- Genre popularity analysis.
- Top actors and their average ratings.
- Duplicate movie title analysis.
- Popularity and vote-count relationship analysis.
- Identification of unusual popularity and vote-count combinations.

### Phase 4: Data Visualization

**Notebook:** `04_visualizations.ipynb`

Created 13 visualizations to explore movie industry patterns.

1. Budget distribution.
2. Runtime distribution.
3. Movie rating distribution.
4. Movie count by genre.
5. Budget versus revenue scatter plot.
6. Popularity versus vote-count scatter plot.
7. Average rating by genre.
8. Movies released per year.
9. Correlation heatmap.
10. Pairplot of important movie features.
11. Budget versus revenue by primary genre.
12. Rating distribution by genre.
13. Average revenue by genre and release decade.

---

## 6. Streamlit Application

The final application was developed using Streamlit and Plotly.

It provides interactive movie analytics through three functional sections.

### Page 1: Filters

Shared sidebar filters are available across Dashboard and Query Explorer.

Features:

- Genre multiselect.
- Release-year range slider.
- Minimum-rating slider.
- Language selectbox.
- Live count of matching movies.
- Persistent filter selections using `st.session_state`.

The selected filters are applied consistently across the Dashboard and Query Explorer.

### Page 2: Dashboard

The Dashboard provides an overview of movie industry performance through KPIs and interactive charts.

**Key Performance Indicators:**

- Total Movies.
- Total Genres.
- Unique Actors.
- Unique Crew Members.

**Visualizations:**

- Top 10 highest-grossing movies.
- Movie distribution by genre.
- Budget versus revenue.
- Average movie rating by genre.
- Movie releases over the years.
- Top 10 actors by movie count.
- Top 10 directors by movie count.

### Page 3: Query Explorer

The Query Explorer allows users to select and explore the 10 SQL analysis questions through a dropdown.

Features:

- Dropdown of saved analytical questions.
- SQL query execution using Python and MySQL.
- Results displayed using `st.dataframe()`.
- Interactive Plotly charts.
- Text-based analytical insights.
- Shared filters applied to query results.

The Action Movies After 2015 query uses the cleaned CSV data because the cleaned dataset contains the `release_year` field used by that analysis. The other SQL questions execute against the MySQL database.

---

## 7. Key Findings, Insights and Recommendations

The following are five important findings from the completed analysis.

### Insight 1: Movie Release Trends

**Finding:** The year 2016 recorded the highest number of movie releases in the dataset, with 121 movies.

**Recommendation:** Movie industry analysts can examine release-year trends to understand production activity and identify periods of higher movie releases.

### Insight 2: Budget and Revenue Relationship

**Finding:** Budget and revenue have a positive correlation of approximately 0.68 in the analyzed dataset.

**Recommendation:** Production budgets should be evaluated alongside expected revenue, market potential, and financial risk. A higher budget alone does not guarantee commercial success.

### Insight 3: Genre Ratings

**Finding:** War was the highest-rated genre, with an average rating of approximately 7.36, considering genres with at least 20 movies.

**Recommendation:** Production companies can study audience responses to highly rated genres when evaluating potential movie concepts and content strategies.

### Insight 4: Genre Popularity

**Finding:** Science Fiction recorded the highest average popularity score among the genres analyzed, at approximately 21.26.

**Recommendation:** Movie producers and marketers can investigate audience interest in Science Fiction and similar genres when planning promotional and content strategies.

### Insight 5: Popularity and Vote Count

**Finding:** Popularity and vote count have a positive correlation of approximately 0.36, indicating that the relationship is not especially strong. The analysis also identified 68 unusual popularity and vote-count combinations.

**Recommendation:** Movie popularity should not be evaluated using a single metric. Analysts should consider popularity, audience votes, ratings, and other performance indicators together.

---

## 8. Key Outcomes

The Reel Insights project successfully demonstrates an end-to-end movie data analytics workflow.

The major outcomes achieved are:

1. **Data Cleaning:** Successfully cleaned six relational datasets, removed duplicate records, checked missing values, and prepared 93,272 records for analysis.

2. **SQL Analysis:** Completed all 10 SQL analytical questions using MySQL, covering movie revenue, genres, actors, directors, keywords, budgets, and ratings.

3. **Pandas Analysis:** Completed 10 Pandas-based analytical questions, including profit, ROI, release trends, runtime outliers, genre popularity, and movie performance patterns.

4. **Data Visualization:** Developed 13 visualizations to identify trends, distributions, relationships, and patterns in movie industry data.

5. **Interactive Streamlit Dashboard:** Built an interactive application with shared filters, movie performance KPIs, and analytical charts.

6. **SQL Query Explorer:** Implemented all 10 analytical queries with tabular results, interactive charts, and written insights.

7. **Shared Filtering:** Implemented genre, release-year, minimum-rating, and language filters with persistent selections across Dashboard and Query Explorer.

8. **MySQL Integration:** Connected the Streamlit application to the MySQL `reel_insights` database using Python's `mysql.connector`.

9. **Business Insights:** Identified important patterns related to movie revenue, ratings, popularity, genre performance, and release trends.

10. **End-to-End Application:** Integrated data analysis, SQL querying, visualization, and interactive exploration into a single Streamlit project.

**Overall Outcome:** The project transforms raw TMDB movie datasets into an interactive analytics solution that enables users to explore movie industry performance and discover meaningful insights through data-driven analysis.

## 9. Project Folder Structure

```text
miniproject-1/
│
├── app.py
├── common_filters.py
├── README.md
├── requirements.txt
│
├── database/
│   └── reel_insights.sql
│
├── pages/
│   └── 3_Query_Explorer.py
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_sql_analysis.ipynb
│   ├── 03_pandas_analysis.ipynb
│   └── 04_visualizations.ipynb
│
└── TMDB_data/
    ├── original datasets
    │
    └── cleaned/
        ├── movies_cleaned.csv
        ├── genres_cleaned.csv
        ├── movie_genres_cleaned.csv
        ├── cast_cleaned.csv
        ├── crew_cleaned.csv
        └── movie_keywords_cleaned.csv
```

---

## 10. Installation and Setup

### Step 1: Install Python dependencies

Open a terminal in the project root directory.

```bash
pip install -r requirements.txt
```

### Step 2: Start MySQL

- Open XAMPP Control Panel.
- Start Apache and MySQL.
- Make sure the `reel_insights` database is available in MySQL.

### Step 3: Configure the database connection

The application uses Python's `mysql.connector` to connect to the local MySQL database.

The current local development configuration is:

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="reel_insights"
)
```

For another environment, update the database connection settings accordingly.

### Step 4: Run the Streamlit application

```bash
streamlit run app.py
```

### Step 5: Open the application

The application will normally be available at:

```text
http://localhost:8501
```

---

## 11. Conclusion

Reel Insights demonstrates an end-to-end data analytics workflow, starting from raw data cleaning and progressing through SQL analysis, Pandas-based exploratory data analysis, data visualization, and interactive dashboard development.

By combining Python, MySQL, Pandas, Plotly, and Streamlit, the project transforms relational movie datasets into meaningful analytical insights.

The final application enables users to explore movie performance, financial trends, genre ratings, actor contributions, director activity, and keyword patterns through interactive filters and query-based visualizations.

---

**Project Title:** An End-to-End Exploratory Data Analysis of the Global Movie Industry (TMDB)

**Dashboard Name:** Reel Insights

**Skills Demonstrated:** Python, Pandas, NumPy, MySQL, SQL, Data Cleaning, Exploratory Data Analysis, Data Visualization, Plotly, Streamlit, and Data Analytics.
