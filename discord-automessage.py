import http.client
import json,time
from config import getCreds
#LOGIN#
conn = http.client.HTTPSConnection("discord.com")
username,password = getCreds()
payload = "{\"login\":\""+username+"\",\"password\":\""+password+"\"}"

headers = {
    'Content-Type': "application/json"
    }

conn.request("POST", "/api/v9/auth/login", payload, headers)

res = conn.getresponse()
data = res.read()
daToken = json.loads(data.decode("utf-8"))["token"]
#LOGIN IS DONE AT THIS POINT#

daCount = 0

def sendMessage(daChannelID, daMessage):
    conn = http.client.HTTPSConnection("discord.com")
    global daCount
    payload = ""

    headers = {
    'authorization': daToken,
    'Content-Type': "application/json"
    }

    conn.request("GET", "/api/v9/channels/"+daChannelID+"/messages", payload, headers)
    payload = "{\"content\": \""+daMessage+"\",\n\"nonce\": "+str(daCount)+",\n\"tts\": false}"
    
    res = conn.getresponse()
    data = res.read()
    print("Payload:"+payload)
    conn.request("POST", "/api/v9/channels/"+str(daChannelID)+"/messages", payload, headers)
    daCount += 1
    time.sleep(.25)
def sendReply(daChannelID, daMessage, msgToReply, pingInReply = False, log = True):
    conn = http.client.HTTPSConnection("discord.com")
    global daCount
    payload = ""

    headers = {
    'authorization': daToken,
    'Content-Type': "application/json"
    }

    payload = """{
    "content": " """+daMessage+""" ",
    "nonce": """+str(daCount)+""",
    "tts": false,
    "message_reference": {
        "channel_id":"""+daChannelID+""",
        "message_id":"""+msgToReply+"""
        }
    }\n"""
    print("Payload:"+payload)
    conn.request("POST", "/api/v9/channels/"+daChannelID+"/messages", payload, headers)
    daCount += 1
    time.sleep(.25)
def getMessages(daChannelID, daRange):
    headers = {
    'authorization': daToken,
    'Content-Type': "application/json"
    }
    conn.request("GET", "/api/v9/channels/"+str(daChannelID)+"/messages", "", headers)
    response = conn.getresponse()
    data = response.read()
    data = json.loads(data.decode("utf-8"))
    return(data[0:daRange])