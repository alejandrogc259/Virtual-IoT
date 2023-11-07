import time
from counterfit_connection import CounterFitConnection
import requests
CounterFitConnection.init('127.0.0.1', 5000)

deviceId = -1
myPollId = -1

def tryToLink(code):
    link = "http://localhost:8080/link"
    body = {
        "code": code
    }
    r = requests.post(url = link, params = body)
    data = r.json()
    global deviceId 
    deviceId = data["id"]
    global myPollId 
    myPollId = data["poll"]["id"]
    print("linked, your deviceId is "+str(deviceId)+" and your pollId is "+str(myPollId))
def sendAnswer(color):
    print("trying to send answer")
    URL = "http://localhost:8080/answers"
    answer = {
        "color": color,
        "poll": {
            "id": 41
        },
        "device":{
            "id": 5
        } 
    }
    r = requests.post(url = URL, json = answer)
    data = r.json()
    print(data)
#tryToLink(8269)
#sendAnswer(1)
while True:
    
    linkbutton = CounterFitConnection.get_sensor_boolean_value(0) # The button returns boolean values, True for pressed and False for released
    numbutton = CounterFitConnection.get_sensor_boolean_value(1)
    nextbutton = CounterFitConnection.get_sensor_boolean_value(2)
    greenbutton = CounterFitConnection.get_sensor_boolean_value(3)
    redbutton = CounterFitConnection.get_sensor_boolean_value(4)




    linking = False
    pressed = False
    i = 0
    code = [-1, -1, -1, -1]
    num = 0
    next = False
    linked = False
    while linkbutton:
        linkbutton = CounterFitConnection.get_sensor_boolean_value(0)
        numbutton = CounterFitConnection.get_sensor_boolean_value(1)
        nextbutton = CounterFitConnection.get_sensor_boolean_value(2)
        linking = True
        
        
        if numbutton and not pressed:
            pressed = True
            num = num+1
            next = False
                   
        if not numbutton:
            pressed = False

        if nextbutton and not next:
                next = True
                code[i] = num
                print(num)
                num = 0
                i = i+1
        if not nextbutton and next:
            next = False
        if i == 4:
            finalCode = code[0]*1000 + code[1]*100 + code[2]*10 + code[3]
            if not linked: 
                tryToLink(finalCode)
                linked = True



    sent = False
    while greenbutton: 
        if deviceId != -1 and myPollId != -1 and not sent:
            sendAnswer(1)
            sent = True

    while redbutton:
        if deviceId != -1 and myPollId != -1 and not sent:
            sendAnswer(2)
            sent = True
    time.sleep(0.5) # Used a short sleep timer as not to miss a button press when the script is on break
