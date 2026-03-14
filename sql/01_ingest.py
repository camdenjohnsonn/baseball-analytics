import pandas as pd
import sqlite3
import os

os.chdir(r"C:\Users\camde\Desktop\baseball_analytics")

conn = sqlite3.connect("data/baseball.db")

tables = {"batting": "data/raw/Batting.csv",
          "pitching": "data/raw/Pitching.csv",
          "people": "data/raw/People.csv", 
          "people_raw": "data/raw/People.csv", 
          "teams": "data/raw/Teams.csv", 
          "salaries": "data/raw/Salaries.csv", 
          "fielding": "data/raw/Fielding.csv", 
          "awards_players": "data/raw/AwardsPlayers.csv", 
          "hall_of_fame": "data/raw/HallOfFame.csv", 
          "appearances": "data/raw/Appearances.csv", 
          "allstar": "data/raw/AllstarFull.csv", 
          "batting_post": "data/raw/BattingPost.csv",
          "series_post": "data/raw/SeriesPost.csv"}

for table_name, filepath in tables.items():
    df = pd.read_csv(filepath)
    df.to_sql(table_name, conn, if_exists="replace", index = False)

conn.close()