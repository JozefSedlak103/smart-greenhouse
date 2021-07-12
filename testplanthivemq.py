import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
from pyDes import *

def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    obj = json.loads(message.payload)
    print(obj)
    #print(userdata)
    if obj['sprinkler'] == 1 and userdata['myobj']['plantID'] == obj['plantID']:
        userdata['myobj']['water'] = 10

current_state = {
    "water" : 0,
    "plantID" : 2
    }
client_userdata = {'myobj': current_state}



plantID = 1
client = mqtt.Client()
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("pespes", "Hackaton2021")
client.connect("0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud", 8883)

subclient = mqtt.Client(userdata=client_userdata)
subclient.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
subclient.username_pw_set("pespes", "Hackaton2021")
subclient.connect("0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud", 8883)
#subclient = mqtt.Client(client_id="tester4387", userdata=client_userdata)
#subclient.connect("broker.hivemq.com")
subclient.subscribe("kpi/iot/hackathon2021/greenhouse/pc")
subclient.on_message = on_message
subclient.loop_start()

now = datetime.now()
for i in range(0, 2):
    print("status=" + str(i))
    print(current_state)
    for y in range(1, 11):
        plantID = y
        water_diff = 0
        if current_state['water'] > 0:
            current_state['water'] -= 1
            water_diff = 10
        time.sleep(1)
        soil_moisture1 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
        soil_moisture2 = [13.1, 15.8, 9.6, 8.5, 7.1, 6.3, 5.5, 5.2, 5.0, 6.1, 6.0, 4.5]
        soil_moisture3 = [3.6, 2.7, 2.4, 2.5, 2.1, 2.3, 2.5, 2.2, 2.0, 2.1, 2.0, 2.5]
        soil_moisture4 = [9.1, 9.8, 9.6, 9.5, 8.1, 8.3, 8.5, 9.2, 8.0, 7.1, 7.0, 7.5]
        soil_moisture5 = [5.1, 5.8, 5.6, 5.5, 5.1, 4.3, 4.5, 4.2, 4.0, 4.1, 4.0, 3.5]
        soil_pH1 = [7.1, 6.8, 6.6, 6.5, 7.1, 7.3]
        soil_pH2 = [4.1, 4.8, 4.6, 4.5, 4.1, 4.3]
        soil_pH3 = [7.1, 7.8, 8.6, 8.5, 7.8, 7.5]
        soil_moisture = soil_moisture1
        soil_pH = soil_pH1
        if plantID == 1 or plantID == 6:
            soil_moisture = soil_moisture1
            soil_pH = soil_pH1
        if plantID == 2 or plantID == 7:
            soil_moisture = soil_moisture2
            soil_pH = soil_pH2
        if plantID == 3 or plantID == 8:
            soil_moisture = soil_moisture3
            soil_pH = soil_pH3
        if plantID == 4 or plantID == 9:
            soil_pH = soil_pH1
            soil_moisture = soil_moisture4
        if plantID == 5 or plantID == 10:
            soil_pH = soil_pH2
            soil_moisture = soil_moisture5
            
        individual_mes = {
        "plantID": plantID,
        "soil_moisture": soil_moisture[i%12] + water_diff,
        "soil_pH": soil_pH[i%6]
        }
        
        #k = des(key="hackaton", padmode=PAD_PKCS5)
        print(json.dumps(individual_mes))
        #print(k.encrypt(json.dumps(individual_mes)).decode("utf-8"))
        client.publish("kpi/iot/hackathon2021/greenhouse/plant2", json.dumps(individual_mes))
        #client.disconnect()
    
#time.sleep(3)
subclient.loop_stop()
subclient.disconnect()