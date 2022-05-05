#
#
#       DataCreator --- Creates multiple MQTT Clients to continously send simulated Data
#
#       Author: Nicoloas Debowiak
#       Editor: Leon Knoke
#       
#       Date: 27.04.2022
#
#

import paho.mqtt.client as mqttClient
import time
from pip._vendor.distlib.compat import raw_input
import ssl
import random
import threading
from timeit import default_timer as timer
import numpy as np
import math
import json

# version fixieren !!!!!

broker_address="mqtt.prodaso.ai"
port =30884


# Release-Plattform
#user = "p-mqtt-u13"
#password = "6nCGS94YE5"
# demo/Local-Plattform
#user = "p-mqtt-u05"
#password = "atrS2DE6xjxm"
# DEV-Plattform
# user = "p-mqtt-u08"
# password = "kO1EIgwWY9"
# Temp
# user = "p-mqtt-u22"
# password = "864rnwKW8R"




Connected = False #global variable for the state of the connection

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global Connected  # Use global variable
        Connected = True  # Signal connection

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    time.sleep(0.1)

# The callback for when a PUBLISH message is received from the server.
def on_log(client, userdata, level, buf):
    time.sleep(0.1)

###############################


def createClient(dataList):

    clId = dataList["clientID"]
    debug = dataList["debug"]
    randomizer = dataList["randomKey"]
    timescale = dataList["timeScale"]

    standbyTimeMin = 60
    standbyTimeMax = 400

    setupTimeMin = 30
    setupTimeMax = 350

    productionTimeMin = 300
    productionTimeMax = 1500

    error1TimeMin = 10
    error1TimeMax = 1400

    error2TimeMin = 30
    error2TimeMax = 600

    error3TimeMin = 40
    error3TimeMax = 150

    clockTimeMin = 20
    clockTimeMax = 30

    
    waitTimeParameter = 2



    randomizer = randomizer % 256
    timescale*=0.1    #  changes all timescales to 10%
    
    #clId = str(num)

    # Parameter
    infotopic = "0.0.1/events/"+str(user)+"/" + str(clId) + "/info"
    parametertopic = "0.0.1/events/"+str(user)+"/" + str(clId) + "/parameter/"

    # Temperatur
    parameterevent_temp = parametertopic + "temperature"
    parametervalue_temp = 60
    # Temperatur
    parameterevent_distance = parametertopic + "distance"
    parametervalue_distance = 60
    # lightSensor
    parameterevent_light = parametertopic + "lightSensor"
    parametervalue_light = 60
    # Temperatur
    parameterevent_acceleration = parametertopic + "acceleration"
    parametervalue_acceleration = 60
    # Temperatur
    parameterevent_angle = parametertopic + "angle"
    parametervalue_angle = 60

    
    clocktopic = "0.0.1/events/"+str(user)+"/" + str(clId) + "/input/0"
    clockevent = "1"


    client1 = mqttClient.Client(str(clId))                           #create client object
    client1.username_pw_set(user, password=password)
    #client1.tls_set(cert_reqs=ssl.CERT_NONE)
    client1.tls_set("mqtt_cloud.cer")
    client1.on_connect = on_connect
    client1.on_message = on_message
    client1.on_log = on_log

    client1.connect(broker_address, port=port)

    client1.loop_start()

    while Connected != True:    #Wait for connection
        time.sleep(0.1)
        if debug==1:
            print("Warte auf Connection")

            print("Connected")

    
    timeStamp = timer()

    waitTime2 = random.randint(100, 200)
    timeStamp2 = timer()
    status = randomizer%3
    #status = 2
    if debug==1:
        print(status)

    waitTime3 = 20
    timeStamp3 = timer()

    IN = ["0","0","0","0","0","0","0","0"]

    tempSin = randomizer + random.randint(-15, 1500)
    tempExp = 10
     
    angleCount = 0
    angleVal = 9

    parameterCount = 0
        
    while True: ##################################################################################################################################
        
        if timeStamp <= timer():                ########################## Parameter
            if parameterCount==0:
                sinTemp = random.randint(-15, 15)/10 + math.sin(tempSin)*20+25 + math.sin(tempSin*3.3)*10 + math.sin(2*tempSin-2*7.2)*7
                tempSin+=0.6
                if status==0:
                    tempExp=100
                    parametervalue_temp = parametervalue_temp*0.5+sinTemp*0.4+tempExp*0.2
                else:
                    tempExp=0
                    parametervalue_temp = parametervalue_temp*0.9+sinTemp*0.02+tempExp*0.08

                parametervalue_distance = random.randint(-15, 15) + math.sin(tempSin)*200 + math.sin(tempSin*4.3)*200 + math.sin(tempSin*9.2) + 500
                parametervalue_acceleration = math.sin(tempSin*0.8)*math.sin(tempSin)*math.sin(1.2*tempSin)*0.3+1
                parametervalue_light = (math.cos(tempSin*0.3) + math.cos(tempSin*0.2) + math.cos(tempSin*0.6))*15+50
                parametervalue_angle = angleVal+angleCount
                if angleCount < 1 :
                    angleCount=random.randint(2, 9)
                    angleVal=random.randint(9, 180)
                angleCount -= 1
            if debug==1 or debug==5:
                #print("parameterevent: ", parameterevent_temp)
                match parameterCount:
                    case 0:
                        print(clId, "| temperautre:", parametervalue_temp)
                    case 1:
                        print(clId, "| distance:", parametervalue_distance)
                    case 2:
                        print(clId, "| light:", parametervalue_light)
                    case 3:
                        print(clId, "| acceleration:", parametervalue_acceleration)
                    case 4:
                        print(clId, "| angle:", parametervalue_angle)

            
            match parameterCount:
                case 0:
                    client1.publish(parameterevent_temp, parametervalue_temp)
                case 1:
                    client1.publish(parameterevent_distance, parametervalue_distance)
                case 2:
                    client1.publish(parameterevent_light, parametervalue_light)
                case 3:
                    client1.publish(parameterevent_acceleration, parametervalue_acceleration)
                case 4:
                    client1.publish(parameterevent_angle, parametervalue_angle)
                    
            parameterCount += 1
            if parameterCount > 4:
                parameterCount=0
            timeStamp += (waitTimeParameter/5)

        if timeStamp2 <= timer():               ########################## Zustände
            if status == 0 or status > 2 :
                IN = ["0","1","1","0","0","0","0","0"] #STANDBY
                status = 1
                waitTime2 = random.randint(standbyTimeMin, standbyTimeMax)
            elif status == 1:
                IN = ["0","1","0","0","0","0","0","0"] #SETUP
                status = 2
                waitTime2 = random.randint(setupTimeMin, setupTimeMax)
            elif status == 2:
                IN = ["0","0","1","0","0","0","0","0"] #PRODUCTION
                status = 0
                waitTime2 = random.randint(productionTimeMin, productionTimeMax)
            
            if random.randint(0, 250)< (randomizer+40)%30+10: 
                status = 3                             # chance for an error
                if random.randint(0, 150)< (randomizer+120)%30+34:
                    IN = ["0","0","0","0","0","0","0","0"] #ERROR 1
                    waitTime2 = random.randint(error1TimeMin, error1TimeMax)
                elif random.randint(0, 50)< (randomizer+35)%15+3:
                    IN = ["0","0","0","1","0","0","0","0"] #ERROR 2
                    waitTime2 = random.randint(error2TimeMin, error2TimeMax)
                elif random.randint(0, 90)< (randomizer+12)%15+12:
                    IN = ["0","0","0","0","1","0","0","0"] #ERROR 3
                    waitTime2 = random.randint(error2TimeMin, error2TimeMax)
                elif random.randint(0, 90)< (randomizer+69)%15+4:
                    IN = ["0","0","0","1","1","0","0","0"] #ERROR 4
                    waitTime2 = random.randint(error2TimeMin, error2TimeMax)
                elif random.randint(0, 90)< (randomizer+20)%15+15:
                    IN = ["0","0","0","0","0","1","0","0"] #ERROR 5
                    waitTime2 = random.randint(error2TimeMin, error2TimeMax)
                elif random.randint(0, 90)< (randomizer+1)%15+16:
                    IN = ["0","0","0","1","0","1","0","0"] #ERROR 6
                    waitTime2 = random.randint(error2TimeMin, error2TimeMax)   
                elif random.randint(0, 60)< (randomizer+90)%15+1:
                    IN = ["0","0","0","0","1","1","0","0"] #ERROR 7
                    waitTime2 = random.randint(error2TimeMin, error2TimeMax)   
                else:
                    IN = ["0","0","0","1","1","1","0","0"] #ERROR 8
                    waitTime2 = random.randint(error3TimeMin, error3TimeMax)
                #status-=1
                #if status<0: 
                 #   status=2

            infoevent = "{\"IN0\":\"" + IN[0] + "\",\"IN1\":\"" + IN[1] + "\",\"IN2\":\"" + IN[2] + "\",\"IN3\":\"" \
                + IN[3] + "\",\"IN4\":\"" + IN[4] + "\",\"IN5\":\"" + IN[5] + "\",\"IN6\":\"" + IN[6] \
                + "\",\"IN7\":\"" + IN[7] + "\"}"
                
            if debug==1 or debug==2 or debug==4:
                match status:
                    case 0:
                        print(clId, "| state: production")
                    case 1:
                        print(clId, "| state: standby")
                    case 2:
                        print(clId, "| state: setup")
                    case 3:
                        print(clId, "| state: error")
                              
                
            client1.publish((infotopic), infoevent)
            
            timeStamp2 += (waitTime2 * timescale)
            

        if timeStamp3 <= timer():                ########################## Clock
            timeStamp3 += waitTime3 * timescale
            if status==0:
                if debug==1 or debug==3 or debug==4:
                    print(clId, "| clockEvent")
                client1.publish(clocktopic, clockevent)
            waitTime3 = random.randint(clockTimeMin, clockTimeMax)


        time.sleep(0.1)


###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################


f = open('clientList.json')

clientList = json.load(f)
user = clientList[0]["user"]
password = clientList[0]["password"]

for x in range(1, len(clientList)):
    Client=threading.Thread(target=createClient, args=(clientList[x],), daemon=True)
    Client.start()


while True:
    time.sleep(0.01)
