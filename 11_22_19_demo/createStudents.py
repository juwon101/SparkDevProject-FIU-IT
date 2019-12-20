import sys
import random
from socket import socket, SOCK_DGRAM, AF_INET
from datetime import datetime
import time
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["FIU"]
table = db["students"]

#read from a file of templates instead of holding a big array of potential names
fnames = ["Daniel", "Juwon", "Maria", "Pablo", "Chris", "John", "Jeniffer"]
lnames = ["Daniel", "Juwon", "Maria", "Pablo", "Chris", "John", "Jeniffer"]
years = ["FRESHMAN","SOPHMORE" ,"JUNIOR", "SENIOR", "GRADUATE"]
mayors = ["CS", "CE", "IT"]
departments = ["   "]
for i in range(0,1000):
    fname = fnames[random.randint(0, 6)]
    lname = lnames[random.randint(0, 6)]
    #can someone format this to look like a real fiu email? thanks!
    table.insert({
        'FNAME' : fname,
        'LNAME' : lname,
        'EMAIL' : fname[:1] + lname[:3] + str(random.randint(0, 9999)) + "@fiu.edu",
        'PID' : str(random.randint(1000000, 9999999)),
        'MAJOR': mayors[random.randint(0, 2)],
        'YEAR': years[random.randint(0, 4)] 
    })
table = db["faculty"]
for i in range(0,1000):
    fname = fnames[random.randint(0, 6)]
    lname = lnames[random.randint(0, 6)]
    table.insert({
        'FNAME' : fname,
        'LNAME' : lname,
        'EMAIL' : fname[:1] + lname[:3] + str(random.randint(0, 9999)) + "@fiu.edu",
        'ID' : str(random.randint(1000000, 9999999)),
        'DEPARTMENT': mayors[random.randint(0, 2)]
    })

