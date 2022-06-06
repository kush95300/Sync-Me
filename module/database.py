import sqlite3
from sqlite3 import Error

def get_users(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # check user user exist
        cur.execute("SELECT  * from users")
        all = cur.fetchall()
        users = [x[0] for x in all]
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return users

def create_user(db_file, username, password, access_key, secret_key):
    """ create a database connection to a SQLite database """
    conn = None
    users = get_users(db_file)
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()


        # check user user exist
        exist = True

        if username not in users:      
            # Create Initial db and user
            statement = "INSERT INTO users (username, password, default_access_key, default_secret_key) VALUES ('{}', '{}', '{}', '{}')".format(username, password, access_key, secret_key)
            cur.execute(statement)
            print(db_file)
            print("User Creted")
            exist = False
        else:
            print("User already exist")  
            exist = True

    except Error as e:
        print("error:",e)
    finally:
        if conn:
            conn.commit()
            conn.close()
    return exist

def validate_user(db_file, username, password):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()


        # check user user exist
        users = get_users(db_file)
        exist = False
        passwd = False

        if username in users:  
            exist = True
            cur.execute("SELECT password from users where username = '{}'".format(username))
            p = cur.fetchone()
            if p[0] == password:
                passwd = True
            else:
                passwd = False
        else:
            exist = False
            passwd = False
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return (exist, passwd)
    