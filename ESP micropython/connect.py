def do_connect(SSID, PASSWORD):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
def on_message(topic, message):
    print('Message "{}" received in topic "{}"'.format(message, topic))    



"""
from umqtt.robust import MQTTClient


client = MQTTClient('pes4894135gdhgd5', 'broker.mqttdashboard.com')
client.set_callback(on_message)
print("connecting")
client.connect()
print("connected")
client.subscribe('kpi/tb/test')
#client.publish('kpi/tb/test', 'test2')
print('Waiting for message...')
client.wait_msg()
print("ending")
client.disconnect()
"""
