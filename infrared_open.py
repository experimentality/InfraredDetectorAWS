'''
Infrared-based door aperture detector using Amazon Web Services

Sebastián Arango Muñoz
Experimentality
'''

import mraa as board
import sys
import argparse
import warnings
import datetime
import json
import time
import updateShadow
#import listenShadow
import boto3

Bot = updateShadow.suscribeToTheThing() #Instantiate the suscription to the thing from Python.


vcc_Emitter = board.Gpio(12)
vcc_Emitter.dir(board.DIR_OUT)
vcc_Receiver = board.Gpio(13)
vcc_Receiver.dir(board.DIR_OUT)
value = board.Aio(0)

vcc_Emitter.write(1)
vcc_Receiver.write(1)

prev_status = False
status = False

while 1:

  val = float(value.read())
  
  if val>700:
    status = True
    print val
    
    if status == True and prev_status == False:
      updateShadow.updateTheShadow('true', Bot) #Refresh Shadow device. Function located in UpdateShadow.py
    
  else:
    status = False
    if status == False and prev_status == True:
      updateShadow.updateTheShadow('false', Bot)
  
  prev_status = status



