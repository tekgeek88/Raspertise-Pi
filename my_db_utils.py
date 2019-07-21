import os.path
import sqlite3


db_parent_directory = "Raspertise"
_db_filename = "raspertise.db"
_current_directory_parent = os.path.split(os.path.dirname(__file__))[0]
_db_file_path = os.path.join(_current_directory_parent, db_parent_directory + '/')
_db_path = DEFAULT_PATH = _db_file_path + _db_filename


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def db_close(conn):
    conn.conn.close()


def get_messages():
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Advertisement")
    result = cursor.fetchall()
    return result


def display_messages(result):
    for i in range(len(result)):
        id, locationId, sponsorId, message, color, dateStart, dateStop = \
            result[i]['id'], result[i]['locationId'], result[i]['sponsorId'], result[i]['message'], result[i]['color'], \
            result[i]['dateStart'], result[i]['dateStop']

        print(
            f"id: {id}, locationId: {locationId}, sponsorId: {sponsorId}, message: {message}, color: {color}, dateStart{dateStart}, dateStop: {dateStop}")


