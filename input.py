import random
import pygame
import time
import mysql.connector
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

while running:
    pygame.event.pump()
    if joystick.get_button(10) == 1:
        sqldelete = "SET SQL_SAFE_UPDATES = 0; DELETE FROM data;"
        mycursor.execute(sqldelete, multi=True)
        db.commit()
        print("start")
        while running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            wheel = joystick.get_axis(0) + 1
            brakepedal = joystick.get_axis(1) + 1
            throttlepedal = joystick.get_axis(2) + 1
            sqlinsert = "INSERT INTO data(wheel, throttle, brake) VALUES (%s, %s, %s)"
            values = wheel, throttlepedal, brakepedal
            mycursor.execute(sqlinsert, values)
            db.commit()
            if joystick.get_button(11) == 1:
                running = False
            time.sleep(0.01)     

print("done")

# print(joystick.get_name()) 
# print (joystick.get_numaxes())
# print (joystick.get_numbuttons())
# print (joystick.get_numhats())
# while True:
#     pygame.event.pump()
#     print ("Wheel:", pygame.joystick.Joystick(1).get_axis(0))
#     print ("Brake:", pygame.joystick.Joystick(1).get_axis(1))
#     print ("Throttle:", pygame.joystick.Joystick(1).get_axis(2))
#     print ("Clutch::",pygame.joystick.Joystick(1).get_axis(3))
#     time.sleep(1)
    

    


    