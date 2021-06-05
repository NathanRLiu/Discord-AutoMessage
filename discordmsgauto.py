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

def sendMessage(daChannelID, daMessage,msgAsReply = False,msgPingReply = False):
    global daCount
    payload = ""

    headers = {
    'authorization': daToken,
    'Content-Type': "application/json"
    }

    conn.request("GET", "/api/v9/channels/"+daChannelID+"/messages", payload, headers)

    res = conn.getresponse()
    data = res.read()
    payload = "{\"content\": \""+daMessage+"\",\n\"nonce\": "+str(daCount)+",\n\"tts\": false}"
    print("Payload:"+payload)
    conn.request("POST", "/api/v9/channels/"+daChannelID+"/messages", payload, headers)
    daCount += 1
    time.sleep(.25)
sendMessage("716140536095965194", "Hello World!")
#print(json.loads(data.decode("utf-8"))[0])