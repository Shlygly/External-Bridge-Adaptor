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

## Contribute

Feel free to contribute
