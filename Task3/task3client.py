#HW3, task 3 Client
#Socket Programming Assignment
#Aaron Schlessman

import socket as s
import time as t

Socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
Address = ('localhost', 12000)
Socket.settimeout(1)

timeouts = 0
pings = []
for x in range(1, 11):
    t_initial = t.time()
    message = '(' + str(x) + ") " + t.ctime(t_initial)

    try:
        send = Socket.sendto(message.encode(), Address)
        print("Sent : " + message)

        recieved, info = Socket.recvfrom(4096)
        print("Received : " + str(recieved))

        t_end = t.time()
        Time = t_end - t_initial
        print("Round Trip Time (seconds): " + str(Time))
        pings.append(Time)

    except s.timeout:
        print("Requested " + str(x) + " timed out")
        timeouts = timeouts + 1

print("closing socket")
Socket.close()

minimum = min(pings)
maximum = max(pings)
average = sum(pings) / len(pings)
Plossrate = (timeouts / 10) * 100
print("Minimum : " + str(minimum))
print("Maximum : " + str(maximum))
print("Average : " + str(average))
print("Packet Loss Rate : %" + str(int(Plossrate)))