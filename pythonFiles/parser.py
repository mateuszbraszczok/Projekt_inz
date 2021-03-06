import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import socket
import sched, time
from datetime import datetime
from variables import tags

dbName = "db.sqlite3"

def keysToString(keys):
    returnValue = ""
    for key in keys:
        returnValue += str(key[0]) + ","
    returnValue += "timestamp"
    return returnValue


def valuesToTuple(values):
    returnValue = tuple()
    for value in values:
        number = float("{:.2f}".format(float(value[1])))
        returnValue += (number,)
    return returnValue


def handling(msg):
    tree = ET.ElementTree(ET.fromstring(msg))
    root = tree.getroot()[2:]

    dataToDatabase = list()
    for child in root:
        if child[0].text in tags:
            dataToDatabase.insert(len(dataToDatabase), [child[0].text, child[1].text]) 

    conn = None
    try:
        conn = sqlite3.connect(dbName)
    except Error as e:
        print(e)

    with conn:
        keys = keysToString(dataToDatabase)
        values = valuesToTuple(dataToDatabase)
        
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        values += (formatted_date,)

        cur = conn.cursor()
        sql = "INSERT INTO Measurements({}) VALUES({})".format(keys, ("?," * len(values))[:-1])
        cur.execute(sql, values)
        conn.commit()
        cur.lastrowid


def main():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(),6340))
    while True:
        starttime = time.time()
        try:
            message ="hi"
            s.send(message.encode("utf-8"))
            time.sleep(0.01)
            msg= s.recv(2048)
            text = msg.decode("utf-8") 
            handling(text)
            time.sleep(1 - ((time.time() - starttime) % 1.0))
        except Exception as e:
            print(e)
            s.close()
            break

if __name__ == "__main__":
    main()
