import paho.mqtt.client as mqtt
import json
from time import sleep
import websockets, ssl
import asyncio


data_changed = False
data = ""

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code))


def on_message(mqttc, obj, msg):
    global data_changed, data  
    # print("data")
    data_changed = True
    data = msg.payload.decode("utf-8")
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_log(mqttc, obj, level, string):
    print(string)





async def ws_client():
    global data_changed, data  
    print("WebSocket: Client Connected.")
    # url = "ws://192.168.29.180:8000/ws/buslocation/2"
    url = "wss://probable-chainsaw-94wwxrw4xqr2p46v-8000.app.github.dev/ws/buslocation/2"
    # Connect to the server
    async with websockets.connect(url) as ws:

        while(True):
            if(data_changed):
                print(data)
                await ws.send(data)
                msg = await ws.recv()
                print(msg)
                print("websocket sent")
                sleep(.5)
                data_changed = False
 
# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_disconnect
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("broker.hivemq.com", 1883, 60000)
mqttc.subscribe("sistgps/#")

mqttc.loop_start()
print("started websocket")
asyncio.run(ws_client()) 





