import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ This method processes the songs files.
    
    It opens the song file json and inserts the data
    into songs & artists tables.
    
    Parameters
    ----------
    cur : cursor
        Cursor of the currenct DB connection.
    filepath : str
        Path to the songs file.
        
    Returns
    -------
    None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[["song_id", "title", "artist_id", "year", "duration"]].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(
        df[["artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude"]]
        .values[0]
    )
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ This method processes the song files.
    
    It opens the log files and inserts the data
    into time, users, & songplays tables.
    
    Parameters
    ----------
    cur : cursor
        Cursor of the currenct DB connection.
    filepath : str
        Path to the songs file.
        
    Returns
    -------
    None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms")
    
    # insert time data records
    time_data = (
        t.values,
        t.dt.hour.values,
        t.dt.day.values,
        t.dt.week.values,
        t.dt.month.values,
        t.dt.year.values,
        t.dt.dayofweek.values
    )
    column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            pd.to_datetime(row.ts, unit="ms"),
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ This method orchestrates the processes.
    
    It loads the files and applies the appropriate function on the files.
    
    Parameters
    ----------
    cur : cursor
        Cursor of the currenct DB connection.
    conn : connection
        Connection to the DB.
    filepath : str
        Filepath to the songs & log files.
    func : function
        Function to apply on the files e.g. process_log_file & process_song_file.
    
    Returns
    -------
    None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ Main function."""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()