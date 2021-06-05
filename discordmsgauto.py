import http.client
import json,time
from config import getCreds, getResponses
#LOGIN#
conn = http.client.HTTPSConnection("discord.com")
username,password = getCreds()
payload = "{\"login\":\""+username+"\",\"password\":\""+password+"\"}"
daComplimentList,daDefenseList,daAngryResponseList,daHappyResponseList,daSadResponseList,daFearfulResponseList, daSurprisedResponseList = getResponses()

headers = {
    'Content-Type': "application/json"
    }

conn.request("POST", "/api/v9/auth/login", payload, headers)

res = conn.getresponse()
data = res.read()
daCount = 0
daToken = json.loads(data.decode("utf-8"))["token"]
#LOGIN IS DONE AT THIS POINT#

def sendMessage(daGuildID, daChannelID, daMessage,msgAsReply = False,msgPingReply = False):
    payload = ""

    headers = {
    'authorization': daToken,
    'Content-Type': "application/json"
    }

    conn.request("GET", "/api/v9/channels/"+daChannelID+"/messages", payload, headers)

    res = conn.getresponse()
    data = res.read()
    print(json.loads(data.decode("utf-8"))[0])
    if msgAsReply == True:
        payload = "{\"content\": \""+daMessage+"\",\n\"nonce\": "+str(daCount)+",\n\"tts\": false,\n\"message_reference\": {\"channel_id\": \""+str(daChannelID)+"\",\n\"guild_id\":\""+str(daGuildID)+"\", \n \"message_id\": \""+str(daMessageID)+"\"},\n"
        if msgPingReply == False:
            payload += "allowed_mentions: {parse: [\"users\", \"roles\", \"everyone\"], \n replied_user: false}"
        payload += "}"
    else:
        payload = "{\"content\": \""+daMessage+"\",\n\"nonce\": "+str(daCount)+",\n\"tts\": false}"
    print("Payload:"+payload)
    conn.request("POST", "/api/v9/channels/"+daChannelID+"/messages", payload, headers)
    daCount += 1
    time.sleep(.25)