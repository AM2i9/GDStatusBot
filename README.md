<h1 float="left">
  <img src="https://cdn.discordapp.com/attachments/675532248493326359/786331970937290762/gdsb_Custom_1.png" styles="margin-bottom:0"/> GDStatusBot
</h1>
 
A discord bot that allows you to show your current progress in a Geometry Dash level through an Embed in discord.

## Installation

First, download the latest release from the [releases page](https://github.com/AM2i9/gdstatusbot/releases). Unzip the file, and move the folder to wherever you want to put it. Open the folder, and open `config.yml`.

### Configuration
`config.yml` can be opened using any text editor. Inside, it will look like this:

```
channel: null
prefix: gd!
token: null
user: null
```

`channel` is a value that is the id of the channel the bot will send its messages to.

`prefix` is the bot prefix, to use its commands

`token` is your discord bot token. This is the only value that you are required to set when downloading the bot.

`null` is your discord user id

To create your bot, and get your token, follow [this guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token), then copy the token and place it in `config.yml`

Once you have created your bot, stay on the same tab where you got your bot token, and scroll down to check off `Server Member Intents`. This will allow the bot to get your username and profile pic on discord.

## Usage

Once you have put a valid token into your config.yml, the bot can now be sucessfully run. To run, double click the exe file, which should open a window like this:

![GDSBWindow](https://cdn.discordapp.com/attachments/675532248493326359/786320078110851132/unknown.png)

Once it has detected Geometry Dash is open, it will say it has found the application and start the bot

![GDSBWindow2](https://cdn.discordapp.com/attachments/675532248493326359/786319975777304636/unknown.png)

Upon your bot starting for the first time, it will give you a code, and ask you to DM it that code. Doing so will allow it to get your discord UserID, and save it in `config.yml`. This is required for the bot to run.

![GDSBWindow3](https://cdn.discordapp.com/attachments/675532248493326359/786761217434976266/unknown.png)

Once linked, you can set your channel.

If you have already invited your bot to your discord server, go to the channel where you want it to send messages, and type your prefix plus `set_channel`. The default prefix is `gd!`, so you would type `gd!set_channel`.

Once your channel is set, you're done! Start playing a level, and an embed should show up to tell you your status throughout the level.

![cycles](https://cdn.discordapp.com/attachments/675532248493326359/786761624408555520/unknown.png)

When you are done playing a level, and you have returned to the main menu, it will show a summary of your progress

![cycles_progress](https://cdn.discordapp.com/attachments/675532248493326359/786761667127672832/unknown.png)

## Multi-user functionality

If you didn't already know, it is possible to run multiple instances of a bot using a singular bot token. You can take advantage of this feature by giving your friends your bot token, and allowing them to use it, meaning you would only need one bot to show everyone's status in a level. 

#### ⚠️However, BE WARNED. You should not give this bot token to people who you do not trust. By giving someone this bot token, you are allowing them the ability to run their own code and bot on it, which can harm you and your server.

You should also note that it is not possible to send your bot token through discord. Discord has a very useful system that scans the message, and if the message contains a bot token, it will automatically alert the owner of the bot token, and invalidate it. To give you friend your bot token, either send it to them using a software other than discord, or put it in a txt file, zip it, and send it to them via discord.

![Multi-user functionality](https://cdn.discordapp.com/attachments/675532248493326359/786758120612823060/unknown.png)

## Bugs
This program is still in its first stages, and may contain bugs and issues. If you find a bug, or have a suggestion for how to make the bot better, submit an issue under the [issues](https://github.com/AM2i9/gdstatusbot/issues) tab.

Also opayc wanted me to put here that he helped test it, so...
