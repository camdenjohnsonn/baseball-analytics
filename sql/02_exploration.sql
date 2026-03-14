SELECT COUNT(DISTINCT playerID) AS total_players
FROM batting;

CREATE VIEW IF NOT EXISTS v_career_hr AS
SELECT p.nameFirst ||' '|| p.nameLast AS player_name, SUM(b.HR) AS career_hr
FROM people p
JOIN batting b on p.playerID = b.playerID
GROUP BY p.playerID
ORDER BY career_hr DESC;

CREATE VIEW IF NOT EXISTS v_best_batting_avg AS
SELECT p.nameFirst ||' '|| p.nameLast AS player_name, b.AB, ROUND(CAST(b.H AS FLOAT)/b.AB, 3) AS batting_average, b.yearID AS year
FROM people p
JOIN batting b on p.playerID = b.playerID
WHERE b.AB >= 400 and b.yearid >= 1900
ORDER BY batting_average DESC;

CREATE VIEW IF NOT EXISTS v_career_ops AS
WITH career_totals AS (
SELECT playerID, SUM(AB) AS career_AB, SUM(H) AS career_H, SUM(BB) AS career_BB, SUM(HBP) AS career_HBP, SUM(SF) AS career_SF, SUM("2B") AS career_2B, SUM("3B") AS career_3B, SUM(HR) AS career_HR, SUM(H) - (SUM("2B") + SUM("3B") + SUM(HR)) AS career_1B
FROM batting
GROUP BY playerID
HAVING career_AB >= 3000
),
ops_calc AS (
SELECT playerID, career_AB, ROUND(CAST(career_H + career_BB + career_HBP AS FLOAT)/NULLIF(career_AB + career_BB + career_HBP + career_SF, 0), 3) AS OBP, ROUND(CAST(career_1B + 2*career_2B + 3*career_3B + 4*career_HR AS FLOAT)/NULLIF(career_AB, 0), 3) AS SLG
FROM career_totals
)
SELECT p.nameFirst ||' '|| p.nameLast AS player_name, o.career_AB, o.OBP, o.SLG, o.OBP + o.SLG AS OPS
FROM people p
JOIN ops_calc o ON p.playerID = o.playerID
ORDER BY OPS DESC;

CREATE VIEW IF NOT EXISTS v_hr_rank_by_yr AS
WITH ranking AS (
SELECT playerID, SUM(HR) AS total_hr, yearID as year, RANK() OVER (PARTITION BY yearid ORDER BY SUM(HR) DESC) AS hr_rank
FROM batting
GROUP BY yearID, playerID
)
SELECT p.nameFirst ||' '|| p.nameLast AS player_name, r.year, r.total_hr, hr_rank
FROM ranking r
JOIN people p ON r.playerID = p.playerID
WHERE year >= 2000 AND hr_rank <= 5
ORDER BY r.year DESC, hr_rank;

CREATE VIEW IF NOT EXISTS v_hr_yoy_change AS 
WITH hr_stats AS(
SELECT yearID, playerID, AB, SUM(HR) as total_hr, LAG(SUM(HR)) OVER (PARTITION BY playerID ORDER BY yearID) AS lag_hr
FROM batting 
WHERE AB >= 300
GROUP BY playerID, yearID
)
SELECT p.nameFirst ||' '|| p.nameLast AS player_name, h.yearID, h.total_hr, h.lag_hr,  h.total_hr - h.lag_hr AS lag_diff
FROM people p
JOIN hr_stats h ON p.playerID = h.playerID
WHERE h.yearID >= 2010
ORDER BY lag_diff DESC;

CREATE VIEW IF NOT EXISTS v_salary_vs_ops AS
WITH ops_cte AS(
SELECT playerID, AB, yearID, ROUND(CAST(H+ BB + HBP AS FLOAT)/NULLIF(AB + BB + HBP + SF, 0), 3) AS OBP, ROUND(CAST (H - ("2B" + "3B" + HR) + 2*"2B" + 3*"3B" + 4*HR AS FLOAT)/NULLIF(AB, 0), 3) as SLG
FROM batting
WHERE AB >= 300
)
SELECT p.nameFirst ||' '|| p.nameLast AS player_name, o.YearID AS year, s.salary, ROUND(o.OBP + o.SLG, 3) AS OPS
FROM ops_cte o
JOIN salaries s ON o.playerID = s.playerID AND o.yearID = s.yearID
JOIN people p ON o.playerID = p.playerID
WHERE year >= 2000
ORDER BY salary DESC;

CREATE VIEW IF NOT EXISTS v_primary_position AS
with pos_counts AS(
    SELECT playerID, POS, SUM(G) as total_games, RANK() OVER (PARTITION BY playerID ORDER BY SUM(G) DESC) AS pos_rank
    FROM fielding
    GROUP BY playerID, POS
)
SELECT playerID, POS as primary_position
FROM pos_counts
WHERE pos_rank = 1;