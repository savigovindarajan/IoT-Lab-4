import json
import logging
import sys

import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# empty dictionary
max_dict = {}

# Counter
my_counter = 0
def lambda_handler(event, context):
    global my_counter
    #TODO1: Get your data
    logger.info(event)
    vehicleid = event["vehicle_id"]
    co2_level = event["co2_level"]
    curr_max = 0
    if vehicleid in max_dict:
        curr_max = max_dict[vehicleid]
    print('Received co2 data event for vehicle {0}, in level {1} , current max {2}'.format( vehicleid, co2_level, curr_max))

    #TODO2: Calculate max CO2 emission
    if curr_max < co2_level:
        print('sending new max co2 data event for vehicle: {0} -> level : {1} '.format( vehicleid, co2_level))
        max_dict[vehicleid] = co2_level
        #TODO3: Return the result
        client.publish(
            topic="co2/max/"+vehicleid,
            payload=json.dumps(
                {"message": "Max co2 observed: {}".format(co2_level),
                 "max_level":co2_level
                }
            ),
        )

    return