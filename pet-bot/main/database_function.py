import sqlite3

def create_database(datafile):
    # connect (or create) a database file
    connect = sqlite3.connect(datafile)
    c = connect.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS userinfo (
            userid TEXT PRIMARY KEY,
            pet_name TEXT,
            date_adopted TEXT,
            hearts_status REAL,
            pet INTEGER,
            pet_log TEXT,
            feed INTEGER,
            feed_log TEXT,
            bath INTEGER,
            bath_log TEXT)
    ''')

    connect.commit()
    connect.close()

def add_data(filename, userid, pet_name, date_adopted, hearts_status, pet, pet_log, feed, feed_log, bath, bath_log):
    """
    Function to add user information in the database.
    """

    # connect to the database
    connect = sqlite3.connect(filename)
    c = connect.cursor()

    c.execute('''
    INSERT INTO userinfo (userid, pet_name, date_adopted, hearts_status, pet, pet_log, feed, feed_log, bath, bath_log)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(userid) DO UPDATE SET
        pet_name = excluded.pet_name,
        date_adopted = excluded.date_adopted,
        hearts_status = excluded.hearts_status,
        pet = excluded.pet,
        pet_log = excluded.pet_log,
        feed = excluded.feed,
        feed_log = excluded.feed_log,
        bath = excluded.bath,
        bath_log = excluded.bath_log
        ''', (userid, pet_name, date_adopted, hearts_status, pet, pet_log, feed, feed_log, bath, bath_log))
    connect.commit()
    connect.close()

def update_data(filename, userid, field, value):
    """
    Function to update information in the database one at a time
    """

    if field not in {"pet_name", "date_adopted", "hearts_status", "pet", "pet_log", "feed", "feed_log", "bath", "bath_log"}:
        raise ValueError("Invalid field name.")

    # connect to the database
    connect = sqlite3.connect(filename)
    c = connect.cursor()

    sql = f"UPDATE userinfo SET {field} = ? WHERE userid = ?"
    c.execute(sql, (value, userid))

    connect.commit()
    connect.close()

def remove_data(filename, userid):
    """
    Function to remove information from database
    """

    connect = sqlite3.connect(filename)
    c = connect.cursor()
    c.execute("DELETE FROM userinfo WHERE userid = ?", (userid,))
    connect.commit()
    connect.close()

def search_data(filename, userid):
    """
    Function to search information in database.
    """

    connect = sqlite3.connect(filename)
    c = connect.cursor()
    c.execute("SELECT 1 FROM userinfo WHERE userid = ?", (userid,))
    user = c.fetchone()
    connect.close()

    # returns True if user exists
    return user is not None

def retrieve_data(filename, userid, field):
    """
    Function to retrieve information from database.
    """

    if field not in {"pet_name", "date_adopted", "hearts_status", "pet", "pet_log", "feed", "feed_log", "bath", "bath_log"}:
        raise ValueError("Invalid field name.")

    connect = sqlite3.connect(filename)
    c = connect.cursor()
    c.execute(f"SELECT {field} FROM userinfo WHERE userid = ?", (userid,))
    value = c.fetchone()[0]
    connect.close()

    # returns True if user exists
    return value