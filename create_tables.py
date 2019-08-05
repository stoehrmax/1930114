import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """Creates the database sparkifydb
    
    Connects to the databases server and creates the database 'sparkifydb'.
    Drops the database if it already exists.
    It returns than the connection and a cursor to the db.
    
    Returns
    -------
    cur : cursor
        postgres cursor for the db
    conn : connection
        postgres connection to the db
    """
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """ Executes the drop statements
    
    Iterates through the drop statements in `drop_table_queries``
    and executes them sequentially.
    
    Parameters
    ----------
    cur : cursor
        postgres cursor for the db
    conn : connection
        postgres connection to the db
    
    Returns
    -------
    none
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ Executes the create statements
    
    Iterates through the create statements in `create_table_queries``
    and executes them sequentially.
    
    Parameters
    ----------
    cur : cursor
        postgres cursor for the db
    conn : connection
        postgres connection to the db
    
    Returns
    -------
    none
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()