import os.path
import sqlite3

import time


db_parent_directory = "Raspertise"
_db_filename = "raspertise.db"

_current_directory_parent = os.path.split(os.path.dirname(__file__))[0]
for i in range(4):
    _current_directory_parent = os.path.split(_current_directory_parent)[0]
print ("Current dir" + _current_directory_parent)

_db_file_path = os.path.join(_current_directory_parent, db_parent_directory + '/')
_db_path = DEFAULT_PATH = _db_file_path + _db_filename


def db_connect(db_path=DEFAULT_PATH):

    con = sqlite3.connect(db_path)
    return con



def get_ads():
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    execute_success = False
    while not execute_success:
        try:
            cursor.execute("SELECT * FROM Advertisement")
            execute_success = True
        except:
            print("Failed, waiting 1 second before retry!")
            time.sleep(1)
    result = cursor.fetchall()
    db_close(conn)
    return result

def db_close(conn):
    conn.close()

def display_messages(result):
    for i in range(len(result)):
        id, locationId, sponsorId, message, color, dateStart, dateStop = \
            result[i]['id'], result[i]['locationId'], result[i]['sponsorId'], result[i]['message'], result[i]['color'], \
            result[i]['dateStart'], result[i]['dateStop']

        print(
            "id: {}, "
            "locationId: {}, sponsorId: {}, message: {}, color: {}, dateStart{}, dateStop: {}".format(id, locationId,sponsorId, message, color, dateStart, dateStop))


