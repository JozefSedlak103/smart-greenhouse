import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    obj = json.loads(message.payload)
    print(obj)
    #print(userdata)
    if obj['sprinkler'] == 1:
        userdata['myobj']['water'] = 10

current_state = {
    "water" : 0
    }
client_userdata = {'myobj': current_state}

plantID = 5

client = mqtt.Client(client_id="tester4386")
client.connect("broker.hivemq.com")

subclient = mqtt.Client(client_id="tester4387", userdata=client_userdata)
subclient.connect("broker.hivemq.com")
subclient.subscribe("kpi/iot/hackathon2021/greenhouse/pc")
subclient.on_message = on_message
subclient.loop_start()

now = datetime.now()
for i in range(0, 3):
    print("status=" + str(i))
    print(current_state)
    water_diff = 0
    if current_state['water'] > 0:
        current_state['water'] -= 1
        water_diff = 10
    time.sleep(1)
    soil_moisture1 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
    soil_moisture2 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
    soil_moisture3 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
    soil_moisture4 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
    soil_moisture5 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
    soil_pH1 = [7.1, 6.8, 6.6, 6.5, 7.1, 7.3]
    soil_pH2 = [4.1, 4.8, 4.6, 4.5, 4.1, 4.3]
    soil_pH3 = [7.1, 7.8, 8.6, 8.5, 7.8, 7.3]
    
    individual_mes = {
    "plantID": plantID,
    "soil_moisture": soil_moisture5[i%12] + water_diff,
    "soil_pH": soil_pH1[i%6]
    }
    
    client.publish("kpi/iot/hackathon2021/greenhouse/plant2", json.dumps(individual_mes))
    #client.disconnect()
    
#time.sleep(3)
subclient.loop_stop()
subclient.disconnect()