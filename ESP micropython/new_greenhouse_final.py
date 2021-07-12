import test
import thermotest
from connect import do_connect
from boot import SSID, PASSWORD
from umqtt.robust import MQTTClient
import umqtt.simple
import ujson
from machine import Pin, PWM
import utime

def on_message(topic, message):
    #print('Message "{}" received in topic "{}"'.format(message, topic))
    if topic == b"kpi/iot/hackathon2021/greenhouse/ac":
        obj = ujson.loads(message.decode("utf-8"))
        #print(obj)
        if obj['heater'] == 1:
            print("heating")
            led=Pin(4,Pin.OUT)
            led.value(1)
        else:   
            print("not heating")
            led=Pin(4,Pin.OUT)
            led.value(0)
        if obj['vent'] == 1:
            print("venting")
            led2=Pin(13,Pin.OUT)
            led2.value(1)
        else:   
            print("not venting")
            led2=Pin(13,Pin.OUT)
            led2.value(0)
        if len(obj) > 2:
            if obj['shaders'] == 1:
                print("shading")
            else:
                print("not shading")
        if len(obj) > 3:
            if obj['light'] == 1:
                print("lighting")
                led2=Pin(25,Pin.OUT)
                led2.value(1)
            else:   
                print("not lighting")
                led2=Pin(25,Pin.OUT)
                led2.value(0)
    if topic == b"kpi/iot/hackathon2021/greenhouse/pc":
        obj = ujson.loads(message.decode("utf-8"))
        #print(obj)
        if obj['sprinkler'] == 1 and 10 == obj['plantID']:
            servo = PWM(Pin(23), freq=50)
            servo.duty(100)
            utime.sleep(1)
            servo.duty(20)
            utime.sleep(2)
            servo.duty(100)
    if topic == b"kpi/iot/hackathon2021/greenhouse/light":
        #obj = ujson.loads(message.decode("utf-8"))
        #print(message)
        if message.decode("utf-8") == "On":
            print("manual lighting")
            led2=Pin(25,Pin.OUT)
            led2.value(1)
        else:   
            print("manual not lighting")
            led2=Pin(25,Pin.OUT)
            led2.value(0)
    
def on_message_light(topic, message):
    if topic == b"kpi/iot/hackathon2021/greenhouse/light":
        #obj = ujson.loads(message.decode("utf-8"))
        #print(message)
        if message.decode("utf-8") == "On":
            print("manual lighting")
            led2=Pin(25,Pin.OUT)
            led2.value(1)
        else:   
            print("manual not lighting")
            led2=Pin(25,Pin.OUT)
            led2.value(0)
#utime.sleep(5)

plantID = 10        
do_connect(SSID, PASSWORD)
SSL_PARAMS = {'server_hostname': '0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud'}
client = MQTTClient(
    client_id = 'pes123',
    server = '0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud',
    port = 8883,
    keepalive = 60,
    ssl=True,
    user='pespes',
    password='Hackaton2021',
    ssl_params=SSL_PARAMS
)
client.set_callback(on_message)
print("connecting")
client.connect()
print("connected")
client.subscribe('kpi/iot/hackathon2021/greenhouse/ac')
client.subscribe('kpi/iot/hackathon2021/greenhouse/pc')
"""
SSL_PARAMS2 = {'server_hostname': '0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud'}
subclient = umqtt.simple.MQTTClient(
    client_id = 'pes125',
    server = '0784feee8a834b3aa62a8445966adf72.s1.eu.hivemq.cloud',
    port = 8883,
    keepalive = 60,
    ssl=True,
    user='pespes',
    password='Hackaton2021',
    ssl_params=SSL_PARAMS2
)

#subclient = umqtt.simple.MQTTClient('pes4894135gdhgkkdl', 'broker.hivemq.com')
subclient.set_callback(on_message_light)
subclient.connect()
subclient.subscribe('kpi/iot/hackathon2021/greenhouse/light')
"""
client.subscribe('kpi/iot/hackathon2021/greenhouse/light')
for i in range(0, 3):
    light_intensity = test.get_light()
    temperature = thermotest.get_temperature()
    humidity = [64, 63, 67, 73, 76, 77, 81, 74, 65, 54, 48, 44, 39, 36, 35, 34, 34, 35, 38, 56, 59, 62, 62, 63]
    water_amount = [80, 65, 40, 20]
    #i = 1
    global_mes = {
        "temperature": temperature,
        "outside_temperature": 21,
        "humidity": humidity[i],
        "light_intensity": light_intensity,
        "water_amount":water_amount[i%4]
        }
    print(global_mes)
    client.publish("kpi/iot/hackathon2021/greenhouse/weather2", ujson.dumps(global_mes))
    client.wait_msg()

    soil_moisture = [9.1, 8.8, 8.6, 8.5, 8.1, 8.3, 8.5, 8.2, 8.0, 8.1, 8.0, 7.5]
    soil_moisture1 = [3.1, 2.8, 2.6, 2.5, 3.1, 3.3, 3.5, 4.2, 5.0, 6.1, 6.0, 4.5]
    soil_moisture2 = [13.1, 15.8, 9.6, 8.5, 7.1, 6.3, 5.5, 5.2, 5.0, 6.1, 6.0, 4.5]
    soil_moisture3 = [3.6, 2.7, 2.4, 2.5, 2.1, 2.3, 2.5, 2.2, 2.0, 2.1, 2.0, 2.5]
    soil_moisture4 = [9.1, 9.8, 9.6, 9.5, 8.1, 8.3, 8.5, 9.2, 8.0, 7.1, 7.0, 7.5]
    soil_moisture5 = [5.1, 5.8, 5.6, 5.5, 5.1, 4.3, 4.5, 4.2, 4.0, 4.1, 4.0, 3.5]
    soil_pH1 = [7.1, 6.8, 6.6, 6.5, 7.1, 7.3]
    soil_pH2 = [4.1, 4.8, 4.6, 4.5, 4.1, 4.3]
    soil_pH3 = [7.1, 7.8, 8.6, 8.5, 7.8, 7.5]
    soil_pH = [7.1, 7.8, 8.6, 8.5, 7.8, 7.3]

    individual_mes = {
        "plantID": 10,
        "soil_moisture": soil_moisture2[i%11],
        "soil_pH": soil_pH2[i%6]
        }
    print(individual_mes)
    client.publish("kpi/iot/hackathon2021/greenhouse/plant2", ujson.dumps(individual_mes))
    client.wait_msg()
    utime.sleep(2)
    #subclient.check_msg()
    client.check_msg()
    #utime.sleep(2)
    #subclient.check_msg()
    client.check_msg()
    print("-------ending cycle-------")
    #utime.sleep(2)
    client.check_msg()
    #subclient.check_msg()
    utime.sleep(2)
    #subclient.check_msg()
    client.check_msg()
#subclient.disconnect()
client.disconnect()


