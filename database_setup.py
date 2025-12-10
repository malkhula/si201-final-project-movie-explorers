import sqlite3

#db setup
conn = sqlite3.connect("movies.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tmdb_movies (
 id INTEGER PRIMARY KEY,
 title TEXT,
 popularity REAL,
 vote_average REAL,
 genre_ids TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tmdb_genres (
 genre_id INTEGER PRIMARY KEY,
 genre_name TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS omdb_movies (
 title TEXT PRIMARY KEY,
 imdb_rating REAL,
 box_office REAL,
 runtime TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tastedive_recommendations (
 movie_title TEXT,
 related_movie TEXT
);
""")

conn.commit()
conn.close()
print("Database and tables created successfully!")

