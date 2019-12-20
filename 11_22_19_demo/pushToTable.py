import pymongo
import os
import time
import datetime
import re
import dateutil.parser
import sys

client = pymongo.MongoClient("localhost", 27017)

db = client["sparkdev"]  # db name

table_name = "test"

if len(sys.argv) == 2:
    table_name = sys.argv[1].lower()

#table = db[table_name]
table = db["sparkdev"]

print(os.getcwd())
path = "/syslog/" + table_name
f = open(path, "r")
ENTRIES = ["BUILDING", "IP", "MAC", "PID", "DATE", "EMAIL"]


f.seek(0)
while True:

    where = f.tell()
    line = f.readline()
    if not line:
        time.sleep(1)
        f.seek(where)
    else:
        print(line)
        values = line.split()[4:]
        print(values)
        post_data = []
        to_insert = {}
        for i, entry in enumerate(ENTRIES):
            if entry == 'DATE':
                print("in Date!")
                my_datetime = dateutil.parser.parse(values[i])
                to_insert[entry] = my_datetime
                print(to_insert[entry])
            elif entry == 'PID' and values[i] == "None":
                to_insert[entry] = None
            else:
                to_insert[entry] = values[i]
                print(to_insert[entry])
        if len(values) == 8:
            if values[6] == 'STUDENT':
                to_insert["TYPE"] = 'STUDENT'
                to_insert["MAJOR"] = values[7] 
            elif values[6] == 'FACULTY':
                to_insert["TYPE"] = 'FACULTY'
                to_insert["DEPARTMENT"] = values[7] 
        post_data.append(to_insert)
        result = table.insert_many(post_data)
        print('one post {0}'.format(result.inserted_ids))
