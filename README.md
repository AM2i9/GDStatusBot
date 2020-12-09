<h1 float="left">
  <img src="https://cdn.discordapp.com/attachments/675532248493326359/786331970937290762/gdsb_Custom_1.png" styles="margin-bottom:0"/> GDStatusBot
</h1>
 
A discord bot that allows you to show your current progress in a Geometry Dash level through an Embed in discord.

## Installation

First, download the latest release from the [releases page](https://github.com/AM2i9/gdstatusbot/releases). Unzip the file, and move the folder to wherever you want to put it. Open the folder, and open `config.yml`.

### Configuration
`config.yml` can be opened using any text editor. Inside, it will look like this:

```
channel: None
prefix: gd!
token: None
```

`channel` is a value that is the id of the channel the bot will send its messages to.

`prefix` is the bot prefix, to use its commands

`token` is your discord bot token. This is the only value that you are required to set when downloading the bot.

To create your bot, and get your token, follow [this guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token), then copy the token and place it in `config.yml`

## Usage

Once you have put a valid token into your config.yml, the bot can now be sucessfully run. To run, double click the exe file, which should open a window like this:

![GDSBWindow](https://cdn.discordapp.com/attachments/675532248493326359/786320078110851132/unknown.png)

Once it has detected Geometry Dash is open, it will say it has found the application and start the bot

![GDSBWindow2](https://cdn.discordapp.com/attachments/675532248493326359/786319975777304636/unknown.png)

If you have already invited your bot to your discord server, go to the channel where you want it to send messages, and type your prefix plus `set_channel`. The default prefix is `gd!`, so you would type `gd!set_channel`.

Once your channel is set, you're done! Start playing a level, and an embed should show up to tell you your status throughout the level.

![cycles](https://cdn.discordapp.com/attachments/675532248493326359/786321268101611539/unknown.png)

When you are done playing a level, and you have returned to the main menu, it will show a summary of your progress

![cycles_progress](https://cdn.discordapp.com/attachments/675532248493326359/786321335596482610/unknown.png)


## Bugs
This program is still in its first stages, and may contain bugs and issues. If you find a bug, or have a suggestion for how to make the bot better, submit an issue under the [issues](https://github.com/AM2i9/gdstatusbot/issues) tab.

Also opayc wanted me to put here that he helped test it, so...
