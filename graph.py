import mysql.connector
import matplotlib.pyplot as plt
import datetime
import numpy as np
import time as t
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="root",
    database ="f1database"
)
mycursor = db.cursor()

wheel = "SELECT Wheel from data"
mycursor.execute(wheel)
wheelresults = mycursor.fetchall()

throttle =  "SELECT Throttle from data"
mycursor.execute(throttle)
throttleresult = mycursor.fetchall()

brake = "SELECT Brake from data"
mycursor.execute(brake)
brakeresult = mycursor.fetchall()

time = "SELECT COUNT(*) from data;"
mycursor.execute(time)
timeresult = mycursor.fetchall()
timeresult = timeresult[0][0]/78

timeresultformat = "{:.3f}".format(timeresult)

timeplot = []
for i in range(0, int(timeresult) + 2):
    timeplot.append(i)

totalentries = []
timerange = 0
for i in range(0, int(len(wheelresults) /78) + 2):
    totalentries.append(timerange)
    timerange += 78


seconds = t.gmtime(timeresult)
timeresultformat = t.strftime("%M:%S:%M",seconds)
timeresultformat = timeresultformat[1:]


plt.figure(figsize=((len(timeplot) + 2) / 4.5 ,4))
plt.gca().margins(x=0)

plt.plot(wheelresults, color = "yellow", label = "Wheel")
plt.plot(throttleresult, color = "green", label = "Throttle")
plt.plot(brakeresult, color = "red", label = "Brake")

plt.xticks(totalentries, timeplot)
plt.xlabel(f"Time {timeresultformat}")
plt.tight_layout()
plt.show()

