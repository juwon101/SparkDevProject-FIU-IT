import sys
import random
from socket import socket, SOCK_DGRAM, AF_INET
from datetime import datetime
import time
import pymongo

serverName = "127.0.0.1"  # change this everytime to send elsewhere
serverPort = 514
clientSocket = socket(AF_INET, SOCK_DGRAM)

#THREE SOURCES OF DATA.
#student table, faculty table, and random guests from which we have 
#add chances later.
client = pymongo.MongoClient("localhost", 27017)
db = client["FIU"]
student_table = db["students"]
faculty_table = db["faculty"]

def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac)) 


names = ["daniel", "Juwon", "Maria", "Pablo", "Chris", "John", "Jeniffer"]

buildings = ["BLUE", "GOLD", "RED"]

while True:

    for x in range(random.randint(1, 5)):
        results = None
        user_type = random.randint(0,2)
        
        building = buildings[random.randint(0, 2)]
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        fiuEmail = None
        pid = None
        message = ""
        if user_type == 0:
            results = student_table.aggregate([{ "$sample": { "size": 1 } }])
            data = results.next()
            pid = data["PID"]
            fiuEmail = data["EMAIL"]
            major = data["MAJOR"]
            message = building + " " + ip + " " + randomMAC() + " " + pid + " " + \
            str(datetime.now().isoformat()) + " " + fiuEmail + " STUDENT " + major + "\n"
        elif user_type == 1:
            results = faculty_table.aggregate([{ "$sample": { "size": 1 } }])
            data = results.next()
            pid = data["ID"]
            fiuEmail = data["EMAIL"]
            major = data["DEPARTMENT"]
            message = building + " " + ip + " " + randomMAC() + " " + pid + " " + \
            str(datetime.now().isoformat()) + " " + fiuEmail + " FACULTY " + major + "\n"
        else:
            pid = "None"
            fiuEmail = names[random.randint(0, 6)] + str(random.randint(0, 9999)) + "@gmail.com"
            message = building + " " + ip + " " + randomMAC() + " " + pid + " " + \
            str(datetime.now().isoformat()) + " " + fiuEmail + "\n"

            #fake_date = datetime(random.randint(2018,2019),random.randint(1,12),random.randint() )
            # ask team 3 for a fake date generator, don't feel like doing it right now

        

        print(message)

        clientSocket.sendto(message.encode(), (serverName, serverPort))

    time.sleep(random.randint(0, 15))
