import sqlite3

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

#average IMDb rating per genre
query_rating = """
SELECT g.genre_name, AVG(o.imdb_rating)
FROM tmdb_movies m
JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
JOIN omdb_movies o ON m.title = o.title
WHERE o.imdb_rating IS NOT NULL
GROUP BY g.genre_name
ORDER BY AVG(o.imdb_rating) DESC;
"""
ratings = cur.execute(query_rating).fetchall()
print("Average IMDb rating per genre:", ratings)

#average box office per genre
query_box = """
SELECT g.genre_name, AVG(o.box_office)/1000000 as avg_box_million
FROM tmdb_movies m
JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
JOIN omdb_movies o ON m.title = o.title
WHERE o.box_office IS NOT NULL
GROUP BY g.genre_name
ORDER BY AVG(o.box_office) DESC;
"""
box_office = cur.execute(query_box).fetchall()
print("Average box office per genre ($M):", box_office)

#average runtime per genre
query_runtime = """
SELECT g.genre_name, AVG(CAST(REPLACE(o.runtime, ' min', '') AS INTEGER)) as avg_runtime
FROM tmdb_movies m
JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
JOIN omdb_movies o ON m.title = o.title
WHERE o.runtime IS NOT NULL
GROUP BY g.genre_name
ORDER BY avg_runtime DESC;
"""
runtime = cur.execute(query_runtime).fetchall()
print("Average runtime per genre (minutes):", runtime)

conn.close()

