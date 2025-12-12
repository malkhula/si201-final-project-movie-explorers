import json
import sqlite3

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

results = {}

#ratings
results["avg_rating"] = cur.execute("""
SELECT g.genre_name, AVG(o.imdb_rating)
FROM tmdb_movies m
JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
JOIN omdb_movies o ON m.title = o.title
WHERE o.imdb_rating IS NOT NULL
GROUP BY g.genre_name;
""").fetchall()

#box office
results["avg_box_office"] = cur.execute("""
SELECT g.genre_name, AVG(o.box_office)
FROM tmdb_movies m
JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
JOIN omdb_movies o ON m.title = o.title
WHERE o.box_office IS NOT NULL
GROUP BY g.genre_name;
""").fetchall()

#runtime
results["avg_runtime"] = cur.execute("""
SELECT g.genre_name, AVG(o.runtime)
FROM tmdb_movies m
JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
JOIN omdb_movies o ON m.title = o.title
WHERE o.runtime IS NOT NULL
GROUP BY g.genre_name;
""").fetchall()

conn.close()

with open("calculation_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Results written to calculation_results.json!")