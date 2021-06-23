import requests
import json,time
import random
import math
import urllib.parse
import pickle

from requests.api import request
from config import getCreds
#LOGIN#
url = "https://discord.com"
username,password = getCreds()
payload = {"login":username,
"password":password}


session = requests.Session()
session.get(url)
daDiscordCookies = session.cookies.get_dict()

headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'Content-Type': "application/json"
    }

loginResponse = requests.request("POST", url+"/api/v9/auth/login", json = payload, headers = headers)


print(loginResponse.text)
daToken = eval(loginResponse.text)["token"]
#LOGIN IS DONE AT THIS POINT#

def createNonce():
    daNonce = ""
    for digit in range(1,16):
        daNonce += str(random.randint(0,9))
    return(daNonce)

def sendMessage(daChannelID, daMessage, log = True):
    headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'authorization': daToken,
    'Content-Type': "application/json"
    }

    payload ={"content": daMessage,
    "nonce": str(createNonce()),
    "tts": False}
    
    if log == True:
        print("Payload:"+str(payload))
    requests.request("POST", url+"/api/v9/channels/"+str(daChannelID)+"/messages", json = payload, headers = headers)
    time.sleep(.25)
def channelInfo(daChannelID):
    print(url+"/channels/"+str(daChannelID))
    daChannelInfo = requests.request("GET", url+"/channels/"+str(daChannelID))
    return daChannelInfo.text
def sendReply(daChannelID, daMessage, msgToReply, pingInReply = True, log = True):

    headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'authorization': daToken,
    'Content-Type': "application/json"
    }

    payload = {
    "content": daMessage,
    "nonce": str(createNonce()),
    "tts": False,
    "message_reference": {
        "channel_id":daChannelID,
        "message_id":msgToReply
        }
    }
    if pingInReply == False:
        payload["allowed_mentions"] = {"parse":["users","roles","everyone"],"replied_user":False}
    if log == True:
        print("Payload:"+str(payload))
  
    requests.request("POST", url+"/api/v9/channels/"+str(daChannelID)+"/messages", json = payload, headers = headers)
    time.sleep(.25)
def getMessages(daChannelID, daRange, log = True):
    headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'authorization': daToken,
    'Content-Type': "application/json"
    }
    if daRange <= 100:
        daURL = url+"/api/v9/channels/"+str(daChannelID)+"/messages?"
        daURL += urllib.parse.urlencode({"limit":daRange})
        if log == True:
            print(url+"/api/v9/channels/"+str(daChannelID)+"/messages")
        daChannelMessages = requests.request("GET", daURL, headers = headers)
        print(daChannelMessages)
        if log == True:
            print(daChannelMessages.text)
        data = json.loads(daChannelMessages.text)
        return(data[0:daRange])
    else:
        returnMessages = []
        lastMessageID = None
        for i in range(math.ceil(daRange/100)):
            print(math.ceil(daRange/100))
            if lastMessageID == None:
                daURL = url+"/api/v9/channels/"+str(daChannelID)+"/messages?"
                daURL += urllib.parse.urlencode({"limit":100})
                daChannelMessages = requests.request("Get",daURL, headers=headers)
                daChannelMessages = json.loads(daChannelMessages.text)
                print(daChannelMessages)
                lastMessageID = daChannelMessages[len(daChannelMessages)-1]
                returnMessages.extend(daChannelMessages)
            else:
                daURL = url+"/api/v9/channels/"+str(daChannelID)+"/messages?"
                daURL += urllib.parse.urlencode({"limit":100,"before":lastMessageID["id"]})
                daChannelMessages = requests.request("Get",daURL, headers=headers)
                daChannelMessages = json.loads(daChannelMessages.text)
                print(daChannelMessages)
                lastMessageID = daChannelMessages[len(daChannelMessages)-1]
                returnMessages.extend(daChannelMessages)
        print(len(returnMessages))
        return(returnMessages[0:daRange])
def exportMessages(daChannelID,fileName = "messages.list",log=True):
    headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'authorization': daToken,
    'Content-Type': "application/json"
    }
    returnMessages = []
    lastMessage = None
    i=0
    daChannelMessages = None
    while True:
        i += 1
        if log==True:
            print(i)
        if lastMessage == None:
            print("lastMessageID is None")
            daURL = url+"/api/v9/channels/"+str(daChannelID)+"/messages?"
            daURL += urllib.parse.urlencode({"limit":100})
            daChannelMessages = requests.request("Get",daURL, headers=headers)
            daChannelMessages = json.loads(daChannelMessages.text)
            lastMessage = daChannelMessages[len(daChannelMessages)-1]
            returnMessages.extend(daChannelMessages)
        else:
            daURL = url+"/api/v9/channels/"+str(daChannelID)+"/messages?"
            daURL += urllib.parse.urlencode({"limit":100,"before":lastMessage["id"]})
            daChannelMessages = requests.request("Get",daURL, headers=headers)
            daChannelMessages = json.loads(daChannelMessages.text)
            print(lastMessage["id"])
            if daChannelMessages == []:
                break
            lastMessage = daChannelMessages[len(daChannelMessages)-1]
            print(len(daChannelMessages))
            returnMessages.extend(daChannelMessages)
    with open(fileName,'wb') as exportFile:
        returnMessages = pickle.dump(returnMessages,exportFile)
    return(returnMessages)

def displayTyping(daChannelID, daDuration):
    times = round(daDuration/1)
    headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'authorization': daToken,
    'Content-Type': "application/json"
    }
    for interval in range(times):
        requests.request("POST", url+"/api/v9/channels/"+str(daChannelID)+"/typing", json = "", headers = headers)
        time.sleep(1)
def searchMessages(daGuildID,isDMs=False,**kwargs):
    headers = {
    'cookie': daDiscordCookies["__dcfduid"],
    'authorization': daToken,
    'Content-Type': "application/json"
    }
    requestResponse = None
    daURL = ""
    if isDMs == False:
        daURL = url+"/api/v9/guilds/"+str(daGuildID)+"/messages/search?"
    else:
        daURL = url+"/api/v9/channels/"+str(daGuildID)+"/messages/search?"
    print(daURL)
    daURL+=urllib.parse.urlencode(kwargs)
    requestResponse = requests.request("GET", daURL, headers = headers)
    return(requestResponse.text)