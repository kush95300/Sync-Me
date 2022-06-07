import sqlite3
from sqlite3 import Error
from module.database import *


def print_users(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # check user user exist
        cur.execute("SELECT  * from users")
        all = cur.fetchall()
        print(all)
        users = [x[0] for x in all]
        print(users)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()


        # check user table exist
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all = cur.fetchall()
        tables = [item for t in all for item in t]
        print(tables)

        if "users" not in tables:
        
            # Create Initial db and user
            script = """CREATE TABLE if not EXISTS users (username, password, default_access_key, default_secret_key);
            INSERT INTO users (username, password) VALUES ('admin','pass');"""
            cur.executescript(script)
            print("Table users created")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_table(r"./.data/account.sql")
    print_users(r"./.data/account.sql")
    

    