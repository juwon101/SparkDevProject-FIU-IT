import pymongo
import os
import time
import datetime
import re
import dateutil.parser

client = pymongo.MongoClient("localhost", 27017)

db = client["sparkdev"]  # db name

table = db['test']

print(os.getcwd())
f = open("/syslog/sparkdev", "r")
ENTRIES = ["BUILDING","IP", "PID", "DATE", "EMAIL"]
#BUILDING = "BLUE"



f.seek(0)
while True:

    where = f.tell()
    line = f.readline()
    if not line:
        time.sleep(1)
        f.seek(where)
    else:
        print(line)
        values = line.split()[5:]
        print(values)
        post_data = []
        to_insert = {}
        for i, entry in enumerate(ENTRIES):
            if entry == 'DATE':
                my_datetime = dateutil.parser.parse(values[i])
                to_insert[entry] = my_datetime
                print(to_insert[entry])
             elif entry == 'PID' and values[i] == "None":
                to_insert[entry] = None
            else:
                to_insert[entry] = values[i]
                print(to_insert[entry])
        if len(values) == 7:
            if values[5] == 'STUDENT':
                to_insert["TYPE"] = 'STUDENT'
                to_insert["MAJOR"] = values[6] 
            elif values[5] == 'FACULTY':
                to_insert["TYPE"] = 'FACULTY'
                to_insert["DEPARTMENT"] = values[6]
        post_data.append(to_insert)
        result = table.insert_many(post_data)
        print('one post {0}'.format(result.inserted_ids))
