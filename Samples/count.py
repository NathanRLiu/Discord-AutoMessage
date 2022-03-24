import sys
sys.path.append("..")
import discord_automessage
import time

counter = 0
channelID=""#change this to your desired channelID
while True:
	counter += 1
	time.sleep(10.001)
	lastNum = discord_automessage.getMessages(channelID,1,True)[0]["content"]
	if (lastNum.isdigit()):
		counter = int(lastNum) + 1
	else:
		counter = 1
	print(lastNum);

	discord_automessage.sendMessage(channelID,counter,False);