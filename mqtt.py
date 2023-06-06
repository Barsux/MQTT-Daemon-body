import paho.mqtt.client as mqtt
from base import Module

class MQTT(Module):
    def __init__(self, flag, name, debug, mqttData):
        super().__init__(flag, name, debug)
        self.data = mqttData
        self.client = mqtt.Client()
        self.client.on_message = self.recv
        self.client.username_pw_set(username=self.data["username"], password=self.data["password"])
        self.client.connect(self.data["host"], self.data["port"])
        self.client.subscribe(self.data["topic"])

        self.tx = self.MQTT_tx(self)
        self.rx = self.MQTT_rx(self)

    def recv(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        self.tx.put(msg)
        self.tx.setReady()
    

    def send(self, msg):
        self.client.publish(self.data["topic"], msg)

    def evaluate(self):
        if self.rx.ready:
            msg = self.rx.get()
            self.send(msg)
            self.rx.clear()
        self.client.loop(0.1)

    
    class MQTT_tx(Module.Queue):
        def __init__(self, broadcaster):
            super().__init__(broadcaster)
            self.instance = broadcaster
    
    class MQTT_rx(Module.Queue):
        def __init__(self, broadcaster):
            super().__init__(broadcaster)
            self.instance = broadcaster