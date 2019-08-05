# Sparkify Database ETL Pipeline
###### By Maximilian Stoehr

## Introduction & Purpose
The purpose of this project is to create a pipeline to provide the data foundation for Sparkify to analyze their customers' behaviour.
It was built with a PostgreSQL database and Python.

To match the requirements, the following steps were executed:
    - an ETL pipeline to extract, transform and load the data from the files to the DB
    - a star schema with the songplays as a centralized fact table
    - a brief interactive walkthrough in form of a Jupyter Notebook
    
## Data
Sparkify base their analysis on two distinct source: the song meta data and the user activity data in form of a log file.

#### Song "Meta" Data:
The song files with the meta data are partitioned by the first three letters of each song's track ID.
Here's an example of a filepath and its corresponding content:

> ##### song_data/A/A/B/TRAABJL12903CDCF1A.json
> 
> {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

#### User Activity Logs:
The user activity was provided as log files. They offer detailed information about customer interaction with Sparkify.
Here's an example of a logfile and its corresponding content:

>  ##### log_data/2018/11/2018-11-12-events.json
>
![User activity](public/log-data.png  "User activity")

## Database Schema
As mentioned in the introduction, a star schema was used to enhance the performance of analytical queries.
Here's an overview of the relationships, columns, foreign keys & primary keys used:
![Star Schmea](public/star_schema.jpg "Star Schema")

The `songplay_id` was implemented as an auto-incremental sequence with PostgreSQLs `SERIAL` datatype and therefore omitted in every `INSERT` statement.

## File Organization
`data` folder contains the song & log data.

`sql_queries.py` contains the SQL queries to be executed by the other scripts.

`create_tables.py` drops and (re)creates the database & corresponding tables.

`test.ipynb` is a Jupyter Notebook to test the ETL processes.

`etl.ipynb` is a Jupyter Notebook which provides an interactive walkthrough of the etl processes.

`etl.py` inherity the main logic of this project. It orchestrates and executes the necessary processes.

## Usage

**1.** Ensure that the data folder is created and all log and song files are uploaded to it.

**2.** Ensure that the postgresql server is running and accepts request from your client.

**3.** Run `python create_tables.py` to create the DB and tables.

**4.** Execute `python etl.py` to insert the data into the tables.


## Troubleshooting

* Run `test.ipynb` to see if all tables have been created and the data was inserted correctly.
* Debug the processes with the interactive `etl.ipynb`.

## Further Enhancements
There are further enhancements which could be implemented:
1. Drop the songplay_id and consider the list of each FK as the PK to ensure no fact is inserted twice.
2. Set `location` as it's own dimension to enhance the geo analytical capabilities
3. Add a genre attribute

## Possible Analytical Queries
The following analytical queries are possible with this database:
1. Which browser do my users use the most?
2. At which time do I have the biggest traffic?
3. Should I focus on premium or freemium users?