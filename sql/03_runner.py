import sqlite3
import pandas as pd
import os


os.chdir(r"C:\Users\camde\Desktop\baseball_analytics")
conn = sqlite3.connect("data/baseball.db")

with open("sql/02_exploration.sql", "r") as f:
    sql = f.read()

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        conn.execute(statement)

conn.commit()

career_hr  = pd.read_sql("SELECT * FROM v_career_hr", conn)
best_avg  = pd.read_sql("SELECT * FROM v_best_batting_avg", conn)
hr_by_yr  = pd.read_sql("SELECT * FROM v_hr_rank_by_yr", conn)
career_ops  = pd.read_sql("SELECT * FROM v_career_ops", conn)
hr_yoy     = pd.read_sql("SELECT * FROM v_hr_yoy_change", conn)
salary_ops = pd.read_sql("SELECT * FROM v_salary_vs_ops", conn)
prim_pos = pd.read_sql("SELECT * FROM v_primary_position", conn)

conn.close()