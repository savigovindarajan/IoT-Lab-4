# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 1
device_end = 6

#Path to the dataset, modify this
data_path = "data/vehicle{}.csv"

#Path to your certificates, modify this

#/Users/savigovindarajan/Documents/Savitha/Education/Lab4/
certificate_formatter = "./certs/vehicle_{}/vehicle_{}.cert.pem"
key_formatter = "./certs/vehicle_{}/vehicle_{}.private.key"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a35zslnq7io05a-ats.iot.us-east-1.amazonaws.com", 8883)
        self.client.configureCredentials("./certs/root-ca-cert.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):
        #TODO4: fill in this function for your publish
        #self.client.subscribeAsync("car/emissions", 0, ackCallback=self.customSubackCallback)
        print("sennding payload ", Payload)
        self.client.publishAsync("car/emissions",Payload , 0, ackCallback=self.customPubackCallback)


print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):

            print("Loading vehicle data %d... ", i)
            #c.publish()
            df = pd.read_csv(data_path.format(i))
            for index, row in df.iterrows():
                message = {}
                message['vehicle_id'] = row['vehicle_id']
                message['co2_level'] = row['vehicle_CO2']
                message['timestamp'] = row['timestep_time']
                message['fuel_level'] = row['vehicle_fuel']
                message['vehicle_HC'] = row['vehicle_HC']
                message['vehicle_NOx'] = row['vehicle_NOx']
                message['vehicle_speed'] = row['vehicle_speed']
                message['version'] = 2

                messageJson = json.dumps(message)
                c.publish(messageJson)

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)




