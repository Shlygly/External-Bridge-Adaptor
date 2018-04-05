# External Bridge Adaptor

Hexchat bridge for discord-irc-sync and slack-irc-sync

## Description

This plugins makes the [IRC-Discord synchronization](https://github.com/Hackndo/discord-irc-sync) or the [IRC Slack synchronization](https://github.com/Hackndo/slack-irc-sync) almost transparent for [Hexchat client](https://hexchat.github.io/)

![ircbridge](https://user-images.githubusercontent.com/11051803/33019729-dcfaf976-cdfb-11e7-84a5-56cc4d4345e6.PNG)

## Features

* Message adaptation
* Events (on join/part/leave/kick/ban) adaptation
* Discord user's nickname added to the list (prefixed with `prefix`, see `/extbridge`)
* Edit configuration with `/extbridge` command
* Reload script with `/extbridge` command

## Documentation

### Installation

Load plugin into Hexchat
1. Window
2. Plugin and Scripts
3. Load script...
4. Select `extBridge.py`

A message confirms script's installation success

### Use

Use `/extbridge` to edit the configuration and reload the script

Usage : `/EXTBRIDGE BRIDGE|CONF|RELOAD`

#### Bridge

Use `BRIDGE` subcommand to manage your bridges

Usage : `/EXTBRIDGE BRIDGE list|add <channel> <server> <bot_nick>|show <index>|set <index> <prop> <value>|del <index>`

##### Add a new bridge

Use `/EXTBRIDGE BRIDGE add <channel> <server> <bot_nick>` to add a new bridge. Replace `<channel>` by the correct channel, `<server>` by the server and `<bot_nick>` by the nick of bridge bot

You can use `*` at the begining of the server url to match multiple server. For example, `*.irc.server.net` will match `foo.irc.server.net` and also `bar.irc.server.net`

You can also just use `/EXTBRIDGE BRIDGE add` to get a preformated command with channel and server set to the current context

Check if it has been correctly added with `/EXTBRIDGE BRIDGE list`

##### List every bridge

Use `/EXTBRIDGE BRIDGE list` to list every bridge index, server and channel

_Example_ :
```
| #   | server                 | channel          |
|-----|------------------------|------------------|
| 0   | *.IRC.Worldnet.Net     | #NewbieContest   |
| 1   | irc.hackerzvoice.net   | #rtfm            |
 ```

##### Edit a bridge

Use `/EXTBRIDGE BRIDGE set <index> <prop> <value>` to set your bridge properties (bot nick, prefix, etc...). Replace `<index>` with the bridge number, `<prop>` with the name of the property and `<value>` with its new value

You can use `/EXTBRIDGE BRIDGE show <index>` to get the list of properties and their current values

_Example_ :
```
bot_channel = #NewbieContest
bot_server = Skadi.IRC.Worldnet.Net
bot_nick = dsc
quit_message = Disconnected from discord
nick_prefix = <DSC>
re_msg_format = ^<([^>]+)> (.+)$
re_cmd_format = ^Cmd by (.+)$
```

##### Delete a bridge

Use `/EXTBRIDGE BRIDGE del <index>` to delete a bridge. Replace `<index>` with the bridge number

#### Configuration

Use `CONF` subcommand to manualy edit the plugin configuration (do it carefully !)

Usage : `/EXTBRIDGE CONF show|get <name>|set <name> <value>`

## Contribute

Feel free to contribute
