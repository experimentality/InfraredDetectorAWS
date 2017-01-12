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

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("property: " + str(payloadDict["state"]["desired"]["open"]))
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
	if responseStatus == "timeout":
		print("Delete request " + token + " time out!")
	if responseStatus == "accepted":
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Delete request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Delete request " + token + " rejected!")

# Usage python basicShadowUpdater.py -e a3btdqpnztfelh.iot.us-west-2.amazonaws.com -r root-CA.crt -c RaspberryPi.cert.pem -k RaspberryPi.private.key

def suscribeToTheThing():
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
	myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowUpdater")
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
	return Bot

def updateTheShadow(access, Bot):
	JSONPayload = '{"state":{"desired":{"open":' + access + '}}}' #JSON with Shadow state.
	Bot.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)

