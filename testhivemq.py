import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    obj = json.loads(message.payload)
    print(obj)
    #print(userdata)
    if obj['heater'] == 1:
        userdata['myobj']['heating'] = True
    else:   
        userdata['myobj']['heating'] = False
    if obj['vent'] == 1:
        userdata['myobj']['venting'] = True
    else:   
        userdata['myobj']['venting'] = False
    if len(obj) > 2:
        if obj['shaders'] == 1:
            userdata['myobj']['shading'] = True
        else:
            userdata['myobj']['shading'] = False
    if len(obj) > 3:
        if obj['light'] == 1:
            userdata['myobj']['lighting'] = True
        else:
            userdata['myobj']['lighting'] = False
    
current_state = {
    "heating" : False,
    "venting" : False,
    "shading" : False,
    "lighting" : False
    }

client_userdata = {'myobj': current_state}
plantID = 1

#client = mqtt.Client(client_id="tester4388")
#client.connect("broker.hivemq.com")
client = mqtt.Client()
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("pespes", "Hackaton2021")
client.connect("0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud", 8883)
#subclient = mqtt.Client(client_id="tester4387", userdata=client_userdata)
#subclient.connect("broker.hivemq.com")
#subclient.subscribe("kpi/iot/hackathon2021/greenhouse/ac")
#subclient.on_message = on_message
#subclient.loop_start()
subclient = mqtt.Client(userdata=client_userdata)
subclient.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
subclient.username_pw_set("pespes", "Hackaton2021")
subclient.connect("0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud", 8883)
subclient.subscribe("kpi/iot/hackathon2021/greenhouse/ac")
subclient.on_message = on_message
subclient.loop_start()

temperature = [3.7, 4.0, 3.2, 2.6, 2.1, 1.9, 1.2, 2.9, 4.8, 6.1, 7.5, 8.6, 9.5, 10.0, 10.5, 10.8, 10.6, 9.9, 7.6, 5.1, 4.0, 3.6, 3.3]
humidity = [64, 63, 67, 73, 76, 77, 81, 74, 65, 54, 48, 44, 39, 36, 35, 34, 34, 35, 38, 56, 59, 62, 62, 63]
light_intensity = [820, 850, 825, 750, 700, 650, 700, 580, 300, 520, 680]
water_amount = [80, 65, 40, 20]

now = datetime.now()
for i in range(0, 23):
    if current_state['heating']:
        temp_diff = 10
    else:
        temp_diff = 0
    if current_state['venting']:
        vent_diff = 10
    else:
        vent_diff = 0
    print("status=" + str(i))
    #print(current_state)
    time.sleep(1)
    
    global_mes = {
    "temperature": temperature[i]+temp_diff-vent_diff,
    "outside_temperature": 21,
    "humidity": humidity[i],
    "light_intensity": light_intensity[i%11],
    "water_amount":water_amount[i%4]
    }
    
    
    client.publish("kpi/iot/hackathon2021/greenhouse/weather2", json.dumps(global_mes))
    #client.disconnect()
    
#time.sleep(3)
subclient.loop_stop()
subclient.disconnect()