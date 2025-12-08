import requests
import sqlite3
import re

#api keys
TMdb_API_KEY = "eb4389c0476b9e7227d02c13c3fa0c0d"
OMdb_API_KEY = "818c3c61"
TASTEDIVE_KEY = "1063543-MovieExp-49866C1E"

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

def fetch_tmdb_genres():
 url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMdb_API_KEY}"  #url for TMdb genres
 data = requests.get(url).json()  #get genres as JSON
 for g in data.get("genres", []):  #loop through each genre
     cur.execute("INSERT OR IGNORE INTO tmdb_genres VALUES (?, ?)", (g["id"], g["name"]))  #insert genre into db
 conn.commit()  #commit changes to db


def fetch_tmdb_movies():
 cur.execute("SELECT COUNT(*) FROM tmdb_movies")  #get current movie count in db
 movie_count = cur.fetchone()[0]  #store the count
 page = movie_count // 20 + 1  #calculate page number for API pagination
 movies_fetched = 0  #initialize counter for new movies
 new_movies = []  #list to store new movie titles
 while movies_fetched < 25:  #loop until 25 new movies are fetched
     url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMdb_API_KEY}&page={page}"  #popular movies URL
     data = requests.get(url).json()  #fetch movie data as JSON
     movies = data.get("results", [])  #get list of movies
     if not movies: break  #stop if no movies are returned
     for m in movies:  #loop through each movie
         cur.execute("""
             INSERT OR IGNORE INTO tmdb_movies (id, title, popularity, vote_average, genre_ids)
             VALUES (?, ?, ?, ?, ?)
         """, (m["id"], m["title"], m["popularity"], m["vote_average"], ",".join(map(str, m["genre_ids"]))))  #insert movie
         cur.execute("SELECT changes()")  #check if insert was successful
         if cur.fetchone()[0] > 0:  #if a new row was added
             new_movies.append(m["title"])  #add title to new_movies list
             movies_fetched += 1  #increment counter
         if movies_fetched >= 25:  #break if 25 new movies fetched
             break
     page += 1  #increment page number for next API call
 conn.commit()  #commit changes to db
 print(f"Fetched {movies_fetched} new movies from TMdb.")  #print number of movies fetched
 return new_movies  #return list of new movie titles


def clean_box_office(value):
 if not value or value in ["N/A", None]:  #if value is missing or N/A
     return None  #return None
 return float(re.sub(r"[^\d]", "", value))  #remove non-digit characters and convert to float


def fetch_omdb(movie_title):
 url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMdb_API_KEY}"  #url for OMdb API
 data = requests.get(url).json()  #fetch movie data as JSON
 if data.get("Response") == "False":  #if movie not found
     cur.execute("""
          INSERT OR REPLACE INTO omdb_movies (title, imdb_rating, box_office, runtime)
          VALUES (?, ?, ?, ?)
      """, (movie_title, None, None, None))  #insert or update movie data
     conn.commit()
     return
 rating = data.get("imdbRating")  #get IMdb rating
 rating = float(rating) if rating not in ["N/A", None] else None  #convert rating to float if valid
 box = clean_box_office(data.get("BoxOffice"))  #clean box office value
 runtime = data.get("Runtime")  #get runtime string
 cur.execute("""
     INSERT OR REPLACE INTO omdb_movies (title, imdb_rating, box_office, runtime)
     VALUES (?, ?, ?, ?)
 """, (movie_title, rating, box, runtime))  #insert or update movie data
 conn.commit()  #commit changes to db


def fetch_tastedive_recommendations(movie_title):
 url = f"https://tastedive.com/api/similar?q={movie_title}&type=movies&limit=20&k={TASTEDIVE_KEY}"  #tastedive API url
 data = requests.get(url).json()  #fetch recommendations as JSON
 recs = data.get("Similar", {}).get("Results", [])  #get list of recommended movies
 if not recs:
     cur.execute("""
          INSERT OR IGNORE INTO tastedive_recommendations (movie_title, related_movie)
          VALUES (?, ?)
      """, (movie_title, "No Recommendation"))  #insert recommendation into db
 else:
    for r in recs:  #loop through recommendations
     cur.execute("INSERT OR IGNORE INTO tastedive_recommendations (movie_title, related_movie) VALUES (?, ?)",
                 (movie_title, r.get("Name")))  #insert recommendation into db
 conn.commit()  #commit changes to db

def fetch_all_data():
 print("Fetching TMdb genres…")  #print status message
 fetch_tmdb_genres()  #fetch TMdb genres
 print("Fetching TMdb movies (25)…")  #print status message
 new_titles = fetch_tmdb_movies()  #fetch 25 new TMdb movies
 if new_titles:  #if there are new movies
     print("Fetching OMdb + TasteDive for new movies…")  #print status
     for title in new_titles:  #loop through new movies
         print("→", title)  #print movie title
         fetch_omdb(title)  #fetch OMdb data
         fetch_tastedive_recommendations(title)  #fetch TasteDive recommendations
 else:
     print("No new movies to fetch OMdb/TasteDive.")  #print message if no new movies

if __name__ == "__main__":
   fetch_all_data()
   conn.close()
   print("Data fetching complete!")
