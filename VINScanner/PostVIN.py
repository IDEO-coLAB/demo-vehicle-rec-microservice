# File : PostVIN.py
# Program is used to Post the Vehicle ID (VIN) in the IOMessage Format to IoFog
# Author: Sooraj Bopanna

import os
import json
import base64
import urllib2
from iofog_container_sdk.client import IoFogClient
from iofog_container_sdk.exception import IoFogException
from iofog_container_sdk.iomessage import IoMessage
from iofog_container_sdk.listener import *

def Post(VIN):
	VINMesg={"VehicleId":VIN}
	JSONVINMesg=json.dumps(VINMesg)
	b64VIN=ConverttoBase64(JSONVINMesg)
	#JSONMesg=ConstructJSONStr(b64VIN)

	#print "JSON Message being sent : ",JSONMesg
	#print "\n"
	#responseMesg=PostVINMessage(JSONMesg)
	responseMesg=SendMesgToFog(b64VIN)

	print " Message Post Response = ",responseMesg
	print "\n"

	return responseMesg

def SendMesgToFog(base64VIN):
        client=IoFogClient()
        msg=IoMessage()
        msg.infotype="application/json"
        msg.infoformat="text/utf-8"
        msg.contentdata=base64VIN
        msg.contextdata=""
        msg.tag="VID"
        msg.groupid=""
        msg.authid=""
        msg.authgroup=""
        msg.hash=""
        msg.previoushash=""
        msg.nonce=""

        try:
                receipt = client.post_message(msg)
        except IoFogException, e:
                print "Exception Sending Message to Fog"
                print "\n"
                print(e)

        return receipt


def ConstructJSONStr(base64VIN):
	MessageVar = {
	"tag":"VehicleIdentifier",
	"groupid":"",
	"sequencenumber":1,
	"sequencetotal":1,
	"priority":0,
	"publisher":os.getenv('SELFNAME'),
	"authid":"",
	"authgroup":"",
	"version":1,
	"chainposition":0,
	"hash":"",
	"previoushash":"",
	"nonce":"",
	"difficultytarget":0.0,
	"infotype":"application/json",
	"infoformat":"text/utf-8",
	"contextdata":"",
	"contentdata":base64VIN
	}
	JSONVINMesg=json.dumps(MessageVar)
	return JSONVINMesg

def PostVINMessage(Mesg):
	url='http://localhost:54321/v2/messages/new'
	req=urllib2.Request(url)
	req.add_header('Content-Type','application/json')
	response=urllib2.urlopen(req,Mesg)
	return response

def ConverttoBase64(VINStr):
	b64VIN=base64.b64encode(str(VINStr))
	return b64VIN
