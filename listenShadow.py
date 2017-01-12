'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import sys
import logging
import time
import json
import getopt
import mraa as board
import time

relay = board.Gpio(8)
relay.dir(board.DIR_OUT)

# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>
#		}
#	}
#}

# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
  print(responseStatus)
  payloadDict = json.loads(payload)
 
#	print("++++++++DELTA++++++++++")
#	print("Temperature: " + str(payloadDict["state"]["Temperature"]))
#	print("Motion: " + str(payloadDict["state"]["Motion"]))
#	print("Person: " + str(payloadDict["state"]["Person"]))
#	print("version: " + str(payloadDict["version"]))
#	print("+++++++++++++++++++++++\n\n")

  if str(payloadDict["state"]["openDoor"])=='true':
    print("Door is open!\n\n")
    relay.write(1)
    time.sleep(1)
  else:
    relay.write(0)

# Read in command-line parameters
useWebsocket = False
host = "a3btdqpnztfelh.iot.us-west-2.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "IR_Relay_Edison-certificate.pem.crt"
privateKeyPath = "IR_Relay_Edison-private.pem.key"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None

myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowDeltaListener")
myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("IR_Relay_Edison", True)

# Listen on deltas
Bot.shadowRegisterDeltaCallback(customShadowCallback_Delta)

# Loop forever
while True:
	pass
