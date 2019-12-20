import pymongo
import time
import datetime

client = pymongo.MongoClient("localhost", 27017)

db = client["sparkdev"]  # db name
table = db['test'] # pick table

# query the table

query = {}

results = table.find(query)

for x in results:
  print(x["EMAIL"])
