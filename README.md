# Discord-AutoMessage #
A robust and versatile solution for automated social interactions

## HOW TO INSTALL ##
1. Open cmd
2. cd into your project directory
3. Run the following commands to make a subtree
```
$ cd C:/PathToMyProject

$ git remote add -f Discord-AutoMessage https://github.com/NathanRLiu/Discord-AutoMessage

$ git merge -s ours --no-commit --allow-unrelated-histories Discord-AutoMessage/main

$ git read-tree --prefix=discAutoMsg/ -u Discord-AutoMessage/main

$ git commit -m "Merge Discord-AutoMessage as a subdirectory"
``` 

4. Run `$ git pull -s subtree Discord-AutoMessage main` to pull new changes

<sub> You can import from a python file within PathToMyProject by using `import discAutoMsg.discord_automessage as discAutoMsg` .<sub>

### OR ###
1. Download the ZIP from the GitHub Repository
2. Extract the ZIP
3. Move the files to the same directory as your project
## HOW TO USE ##
1. Make sure you put your email and password in the config.py folder, and double check the code you have downloaded because you don't want your sensitive data leaked
2. You can now import the functions of the module by simply calling 
`import discord-automessage`
3. After importing the module, you can now reference its functions by calling `discord-automessage.functionName`, for example: 
`discord-automessage.sendMessage(channelID,"Hello World!")`
## LIST OF FUNCTIONS ##
`sendMessage(daChannelID, daMessage)`

### WHERE: ###
* daChannelID is a `string` which is passed as the ID of the channel.
* daMessage is a `string` which is passed as the content of the message.

`sendReply(daChannelID, daMessage, msgToReply)`

### WHERE: ###
* daChannelID is a `string` or `int` which is passed as the ID of the channel.
* daMessage is a `string` which is passed as the content of the message.
* msgToReply is a `string` or `int` which is the messageID of the message to reply to

`getMessages(daChannelID, daRange)`

### WHERE: ###
* daChannelID is a `string` which is passed as the ID of the channel.
* daRange is an `int` which denotes how many messages you want returned.
