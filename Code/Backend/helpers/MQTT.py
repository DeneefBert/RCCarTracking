import paho.mqtt.client as mqtt
import time
import math

address = '192.168.168.168'
user = 'fluvisol'
password = 'fluvisol'
topic = 'sensors/+'

def decode(a):
    string_a = a.decode(encoding='utf-8')
    return string_a

class Wireless:
    def __init__(self, address = address, user = user, password = password, topic = topic):
        self.address = address
        self.user = user
        self.password = password
        self.topic = topic
        # Dict with values from sensors. Easy to add more if desired, more efficient than earlier version of just declaring variables
        self.vals = {
            "accx" : 0,
            "accy" : 0,
            "accz" : 0,
            "acc" : 0,
            "temp" : 0,
            "ldr" : 0,
        }
        self.outvals = {
            "actuators/override": 0,
            "actuators/lights": 0,
            "actuators/sounds": 400,
            "actuators/intensity": 50
        }

    def on_connect_in(self, client, userdata, flags, rc):
        print(f'Connected with result code {str(rc)}')
        client.subscribe(self.topic)
    
    def on_message(self, client, userdata, msg):
        """The callback for when a PUBLISH message is received from the server."""
        sorting = msg.topic
        value = decode(msg.payload)
        if sorting[:8] == "sensors/" and sorting != "sensors/timing":
            t = sorting[8:]
            self.vals[t] = float(value)
        if sorting == "sensors/timing":
            self.vals["acc"] = round(math.sqrt(((self.vals["accx"] / 8192.0) ** 2 + (self.vals["accy"] / 8192.0) ** 2 + (self.vals["accz"] / 8192.0) ** 2)),2)

    def publish(self, client):
        while True:
            time.sleep(1)
            for i in self.outvals.keys():
                topic = i
                msg = self.outvals[i]
                client.publish(topic, msg)
            

    def setup(self):
        mqtt_client = mqtt.Client("pi_in")
        mqtt_client.username_pw_set(self.user, self.password)
        mqtt_client.on_connect = self.on_connect_in
        mqtt_client.on_message = self.on_message
        mqtt_client.connect(self.address, 1883)
        mqtt_client.loop_start()
        self.publish(mqtt_client)
        