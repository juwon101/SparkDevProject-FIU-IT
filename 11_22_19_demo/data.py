import sys
import random
from socket import socket, SOCK_DGRAM, AF_INET
from datetime import datetime
import time

serverName = "127.0.0.1"  # change this everytime
serverPort = 514
clientSocket = socket(AF_INET, SOCK_DGRAM)

names = ["daniel", "Juwon", "Maria", "Pablo", "Chris", "John", "Jeniffer"]

buildings = ["BLUE", "GOLD", "RED"]

while True:

    for x in range(random.randint(1, 5)):

        building = buildings[random.randint(0, 2)]

        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

        pid = str(random.randint(1000000, 9999999))

        fiuEmail = names[random.randint(0, 6)] + "@fiu.edu"

        #fake_date = datetime(random.randint(2018,2019),random.randint(1,12),random.randint() )
        # ask team 3 for a fake date generator, don't feel like doing it right now

        message = building + " " + ip + " " + pid + " " + \
            str(datetime.now().isoformat()) + " " + fiuEmail + "\n"

        print(message)

        clientSocket.sendto(message.encode(), (serverName, serverPort))

    time.sleep(random.randint(0, 7))
