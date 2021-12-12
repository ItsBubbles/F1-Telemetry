import random
from matplotlib.pyplot import get
import pygame
import time
import mysql.connector
import numpy as np
import cv2
from PIL import ImageGrab





pygame.joystick.init()
pygame.display.init()
joystick = pygame.joystick.Joystick(1)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="root",
    database ="f1Database"
)
mycursor = db.cursor()
running = True
dbrunning = True
laprunning = True

# mycursor.execute("DELETE FROM data;")
# db.commit()


def createtable(lap):
    mycursor.execute(f"CREATE TABLE lap{lap}(wheel FLOAT, throttle FLOAT, brake FLOAT)")
lap = 0
while running:
    pygame.event.pump()
    if joystick.get_button(10) == 1:
        mycursor.execute(f"CREATE TABLE lap0(wheel FLOAT, throttle FLOAT, brake FLOAT)")
        print("start")
        while laprunning:
            pygame.event.pump()
            if joystick.get_button(3) == 1:
                time.sleep(0.1)
                while dbrunning:
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    wheel = joystick.get_axis(0) + 1
                    brakepedal = joystick.get_axis(1) + 1
                    throttlepedal = joystick.get_axis(2) + 1
                    sqlinsert = f"INSERT INTO lap{lap}(wheel, throttle, brake) VALUES (%s, %s, %s)"
                    values = wheel, throttlepedal, brakepedal
                    mycursor.execute(sqlinsert, values)
                    db.commit()
                    if joystick.get_button(3) == 1:
                        lap += 1
                        time.sleep(0.1)
                        createtable(lap)
                        print(f"lap {lap}")
                    if joystick.get_button(10) == 1:
                        print("working")
                        dbrunning = False
                        laprunning = False
                        running = False       
                     

                    time.sleep(0.01)     

print("done")


# print(joystick.get_name()) 
# print (joystick.get_numaxes())
# print (joystick.get_numbuttons()) 
# print (joystick.get_numhats())
# while True:
#     pygame.event.pump()
#     # print ("Wheel:", pygame.joystick.Joystick(1).get_axis(0))
#     # print ("Brake:", pygame.joystick.Joystick(1).get_axis(1))
#     # print ("Throttle:", pygame.joystick.Joystick(1).get_axis(2))
#     # print ("Clutch::",pygame.joystick.Joystick(1).get_axis(3))
#     print(joystick.get_button(3))
    

    


    