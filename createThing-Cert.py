################################################### Connecting to AWS
import boto3

import json
import os
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
from urllib3.connectionpool import xrange

thingArn = ''
thingId = ''
thingName = ''
#thingName = ''.join(["" for n in xrange(15)])
defaultPolicyName = 'IOTTestPolicy'


###################################################

def createThing():
    global thingClient
    thingResponse = thingClient.create_thing(thingName=thingName)
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
        createCertificate()


def createCertificate():
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
        setAsActive=True,
       # certificatepemoutfile = (thingName + "certificatePem")
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']
    publicKeyfilename = os.path.join('certificates/'+thingName, thingName+'_public.key')
    privateKeyfilename = os.path.join('certificates/'+thingName,thingName + '_private.key')
    certificatePemKeyfilename = os.path.join('certificates/'+thingName,thingName + 'cert.pem')
    #filepath = os.path.join('c:/your/full/path', 'filename')
    if not os.path.exists('certificates/'+thingName):
        os.makedirs('certificates/'+thingName)
   # os.makedirs('certificates/'+thingName)
    with open(publicKeyfilename, 'w') as outfile:
        outfile.write(PublicKey)
    with open(privateKeyfilename, 'w') as outfile:
        outfile.write(PrivateKey)
    with open(certificatePemKeyfilename, 'w') as outfile:
        outfile.write(certificatePem)

    response = thingClient.attach_policy(
        policyName=defaultPolicyName,
        target=certificateArn
    )
    response = thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )


thingClient = boto3.client('iot')
for i in range(0, 5):
    thingName = "Thing"+str(i+1)
    createThing()
