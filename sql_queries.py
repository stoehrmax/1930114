# DROP TABLES

# Define drop statement for more conciseness
drop_statement = "DROP TABLE IF EXISTS"

# Define list of tables for more conciseness
tables = ["songplayes", "users", "songs", "artists", "time"]

# List comprehension instead of simple list definition
# Old list kept as a comment
# Old:
# drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
# With list comprehension:
drop_table_queries = [drop_statement + " " + table for table in tables]

# Not needed anymore
# songplay_table_drop = ""
# user_table_drop = ""
# song_table_drop = ""
# artist_table_drop = ""
# time_table_drop = ""

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
songplay_id serial PRIMARY KEY,
start_time timestamptz NOT NULL,
user_id int NOT NULL,
level text NOT NULL,
song_id text NOT NULL,
artist_id text NOT NULL,
session_id int NOT NULL,
location text,
user_agent text
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id int PRIMARY KEY,
first_name text NOT NULL,
last_name text NOT NULL,
gender text,
level text NOT NULL
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
song_id text PRIMARY KEY,
title text NOT NULL,
artist_id text NOT NULL,
year int,
duration numeric
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id text PRIMARY KEY,
name text NOT NULL,
location text,
latitude numeric,
longitude numeric
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
start_time timestamptz PRIMARY KEY,
hour int NOT NULL,
day int NOT NULL,
week int NOT NULL,
month int NOT NULL,
year int NOT NULL,
weekday int NOT NULL
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays(
start_time,
user_id,
level,
song_id,
artist_id,
session_id,
location,
user_agent
)
VALUES (
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s
)
""")

user_table_insert = ("""
INSERT INTO users(
user_id,
first_name,
last_name,
gender,
level
)
VALUES(
%s,
%s,
%s,
%s,
%s
)
ON CONFLICT (user_id)
DO UPDATE
SET 
level = EXCLUDED.level,
last_name = EXCLUDED.last_name
""")

song_table_insert = ("""
INSERT INTO songs(
song_id,
title,
artist_id,
year,
duration
)
VALUES(
%s,
%s,
%s,
%s,
%s
)
ON CONFLICT (song_id)
DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists(
artist_id,
name,
location,
latitude,
longitude
)
VALUES(
%s,
%s,
%s,
%s,
%s
)
ON CONFLICT (artist_id)
DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time(
start_time,
hour,
day,
week,
month,
year,
weekday
)
VALUES(
%s,
%s,
%s,
%s,
%s,
%s,
%s
)
ON CONFLICT (start_time)
DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id from songs s join artists a on s.artist_id = a.artist_id
WHERE s.title LIKE %s
AND a.name LIKE %s
AND round(s.duration) = round(%s)
LIMIT 1
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
