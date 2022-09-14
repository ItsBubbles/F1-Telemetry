import matplotlib.pyplot as plt
import sqlite3
from time import strftime, gmtime


connection = sqlite3.connect('f1Database.db')
cursor = connection.cursor()

def lapdata(lap):

    wheel = f"SELECT Wheel from lap{lap}"
    cursor.execute(wheel)
    wheelresults = cursor.fetchall()

    throttle = f"SELECT Throttle from lap{lap}"
    cursor.execute(throttle)
    throttleresult = cursor.fetchall()

    brake = f"SELECT Brake from lap{lap}"
    cursor.execute(brake)
    brakeresult = cursor.fetchall()

    lapTimeQuery = f"SELECT lapTime from lap{lap} ORDER BY lapTime DESC LIMIT 1"
    cursor.execute(lapTimeQuery)
    lapTime = (cursor.fetchall()[0][0])

    timeArray = []
    for i in range(int(lapTime) + 2):
        timeArray.append(strftime("%M:%S", gmtime(i)))

    totalSpacing = []
    timeRange = 0
    for i in range(int(lapTime) + 2):
        totalSpacing.append(timeRange)
        timeRange+= len(wheelresults)/lapTime

    lapTime = strftime("%M:%S%MS", gmtime(lapTime))[:-2]

    plt.figure(figsize=(len(totalSpacing)/4, 4))
  
    plt.plot(wheelresults, color = "yellow", label = "Wheel")
    plt.plot(throttleresult, color = "green", label = "Throttle")
    plt.plot(brakeresult, color = "red", label = "Brake")

    plt.xticks(fontsize=10, rotation=90)
    plt.xticks(totalSpacing, timeArray)

    plt.title(f"Lap {lap}")
    plt.xlabel(f"Time: {lapTime[1:]}")
    plt.tight_layout()
lapdata(0)
plt.show()