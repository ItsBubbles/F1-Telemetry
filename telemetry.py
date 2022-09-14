import socket
from ArrayStructureF1 import * 
from struct import * 
import pygame
import sqlite3
from telemetry import *

UDP_IP = "127.0.0.1" # UDP listen IP-address
UDP_PORT = 20777 # UDP listen port
PACKET_SIZE = 1289 # Amount of bytes in packet
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP Socket
udp.bind((UDP_IP, UDP_PORT)) # Bind socket to IP and port

pygame.joystick.init()
pygame.display.init()
joystick = pygame.joystick.Joystick(0)

connection = sqlite3.connect('f1Database.db')
cursor = connection.cursor()

lastLap = 0
currentLap=0
print ("F1 Telemetry ready")

def getValByName(name):
    global returnData
    for x in range(0, len(returnData)):
        if returnData[x][0] == name: 
            return returnData[x][1]
    return -1 

cursor.execute(f"""CREATE TABLE IF NOT EXISTS lap{lastLap}(wheel FLOAT, throttle FLOAT, brake FLOAT, lapTime FLOAT)""")

running = False
while True:
    pygame.event.pump()
    if joystick.get_button(10) == 1:
        running = True
  
    while running:
        pygame.event.pump()
        index = 0; # Set starting index
        data, addr = udp.recvfrom(PACKET_SIZE) 
        for x in range(0, len(returnData)): 
            size = 4 if returnData[x][2] == 'f' else 1 
            returnData[x][1] = unpack('<' + returnData[x][2], data[index:index+size])[0]
            index += size


      
        wheel = joystick.get_axis(0) + 1
        brakepedal = joystick.get_axis(1) + 1
        throttlepedal = joystick.get_axis(5) + 1

        cursor.execute(f"INSERT INTO lap{currentLap}(wheel, throttle, brake)VALUES ({wheel}, {throttlepedal}, {brakepedal})")

        connection.commit()
        currentLap = int(getValByName("m_lap"))
        print(currentLap)

        if currentLap-1 == lastLap:
            print("Working")
            lastLap = int(getValByName("m_lap"))
            lapTime = getValByName("m_last_lap_time")
            cursor.execute(f"INSERT INTO lap{currentLap - 1}(lapTime) VALUES ({lapTime})")
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS lap{currentLap}(wheel FLOAT, throttle FLOAT, brake FLOAT, lapTime Float)""")  
            connection.commit()
            
        if joystick.get_button(10) == 1:
            running = False