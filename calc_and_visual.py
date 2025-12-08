import sqlite3
import matplotlib.pyplot as plt
import numpy as np


colors = ["#e8d8e0","#aebbdb","#dbc4bc","#ecd8d7","#f4a29d",
         "#cad69e","#cbaedb","#d6bf9f","#b4cbe9","#ece6a2"]


conn = sqlite3.connect("movies.db")
cur = conn.cursor()


def calc_avg_rating_per_genre():
 query = """
 SELECT g.genre_name, AVG(o.imdb_rating)
 FROM tmdb_movies m
 JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
 JOIN omdb_movies o ON m.title = o.title
 WHERE o.imdb_rating IS NOT NULL
 GROUP BY g.genre_name
 ORDER BY AVG(o.imdb_rating) DESC;
 """  #SQL to calculate average IMdb rating per genre
 return cur.execute(query).fetchall()  #execute & return results


def calc_avg_boxoffice_per_genre():
 query = """
 SELECT g.genre_name, AVG(o.box_office)/1000000 as avg_box_million
 FROM tmdb_movies m
 JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
 JOIN omdb_movies o ON m.title = o.title
 WHERE o.box_office IS NOT NULL
 GROUP BY g.genre_name
 ORDER BY AVG(o.box_office) DESC;
 """  #SQL to calculate average box office per genre in millions
 return cur.execute(query).fetchall()  #execute & return results


def calc_avg_runtime_per_genre():
 query = """
 SELECT g.genre_name, AVG(CAST(REPLACE(o.runtime, ' min', '') AS INTEGER)) as avg_runtime
 FROM tmdb_movies m
 JOIN tmdb_genres g ON instr(m.genre_ids, g.genre_id) > 0
 JOIN omdb_movies o ON m.title = o.title
 WHERE o.runtime IS NOT NULL
 GROUP BY g.genre_name
 ORDER BY avg_runtime DESC;
 """  #SQL to calculate average runtime per genre
 return cur.execute(query).fetchall()  #execute & return results


#visuals
colors = ["#e8d8e0","#aebbdb","#dbc4bc","#ecd8d7","#f4a29d",
        "#cad69e","#cbaedb","#d6bf9f","#b4cbe9","#ece6a2"]


def plot_avg_rating(data):
  labels = [row[0] for row in data]  #extract genre names
  values = [row[1] for row in data]  #extract average IMdb ratings
  color_list = [colors[i % len(colors)] for i in range(len(labels))]  #colors
  plt.figure(figsize=(10,6))  #set figure size
  plt.bar(labels, values, color=color_list)  #create bar chart with color palette
  plt.title("Average IMdb Rating per Genre")  #set plot title
  plt.ylabel("IMdb Rating")  #set y axis label
  plt.ylim(0, 10)  #set yaxis limits from 0 to 10
  plt.yticks(np.arange(0, 10.5, 0.5))  #yaxis ticks every 0.5
  plt.xticks(rotation=45, ha='right')  #rotate xaxis labels for readability
  plt.grid(True, axis='y', alpha=0.3)  #add horizontal gridlines
  plt.tight_layout()  #adjust layout to fit labels
  plt.show()  #display plot


def plot_avg_boxoffice(data):
  labels = [row[0] for row in data]  #extract genre names
  values = [row[1] for row in data]  #extract average box office values
  color_list = [colors[i % len(colors)] for i in range(len(labels))]  #colors
  plt.figure(figsize=(10,6))  #set figure size
  plt.barh(labels, values, color=color_list)  #create horizontal bar chart
  plt.title("Average Box Office per Genre ($ Millions)")  #set title
  plt.xlabel("Box Office ($M)")  #label xaxis
  plt.xlim(0, max(values)*1.2 if values else 1)  #extend xaxis slightly beyond max valu
  plt.xticks(np.linspace(0, max(values)*1.2, 10))  #set 10 evenly spaced xticks
  plt.grid(True, axis='x', alpha=0.3)  #add vertical gridlines
  plt.tight_layout()  #adjust layout
  plt.show()  #display plot


def plot_avg_runtime(data):
  labels = [row[0] for row in data]  #extract genre names
  values = [row[1] for row in data]  #extract average runtime values
  color_list = [colors[i % len(colors)] for i in range(len(labels))]  #colors
  plt.figure(figsize=(10,6))  #set figure size
  for i in range(len(labels)-1):  #draw line segments connecting each point
      plt.plot(labels[i:i+2], values[i:i+2], color=color_list[i], linewidth=2)  #line segment
  plt.scatter(labels, values, color=color_list, s=120)  #add points with colors
  plt.title("Average Runtime per Genre")  #set title
  plt.ylabel("Runtime (minutes)")  #label yaxis
  plt.ylim(0, max(values)*1.2 if values else 1)  #extend yaxis beyond max value
  plt.yticks(np.arange(0, max(values)*1.2, 10))  #set yticks every 10 minutes
  plt.xticks(rotation=45, ha='right')  #rotate x axis labels
  plt.grid(True, alpha=0.3)  #add gridlines
  plt.tight_layout()  #adjust layout
  plt.show()  #display plot

if __name__ == "__main__":
   ratings = calc_avg_rating_per_genre()
   plot_avg_rating(ratings)

   box = calc_avg_boxoffice_per_genre()
   plot_avg_boxoffice(box)

   runtime = calc_avg_runtime_per_genre()
   plot_avg_runtime(runtime)

   conn.close()