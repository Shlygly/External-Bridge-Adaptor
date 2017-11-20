import hexchat
import re

__module_name__ = 'External Bridge Adaptor'
__module_version__ = '1.2'
__module_description__ = 'Adapt Hexchat UI for external bridges'
__author__ = 'Stockage'

def InitPref(name, default_value):
    value = hexchat.get_pluginpref(name)
    if (value is None):
        value = default_value
        hexchat.set_pluginpref(name, value)
    return value

def LoadPrefs():
    global bot_nick, bot_vhost, quit_message, nick_prefix, re_msg_format, re_cmd_format, re_join_format, re_quit_format, re_rename_format
    bot_nick = InitPref("bot_nick", "dsc")
    bot_vhost = InitPref("bot_vhost", "discord.newbiecontest.org")
    quit_message = InitPref("quit_message", "Disconnected from discord")
    nick_prefix = InitPref("nick_prefix", "<DSC>")
    re_msg_format = InitPref("re_msg_format", "^<([^>]+)> (.+)$")
    re_cmd_format = InitPref("re_cmd_format", "^Cmd by (.+)$")
    re_join_format = InitPref("re_join_format", "^(.+) has joined$")
    re_quit_format = InitPref("re_quit_format", "^(.+) has quit$")
    re_rename_format = InitPref("re_rename_format", "^(.+) is now known as (.+)$")

LoadPrefs()

cmd_nick = None

def EmitMsg(nick, message, mode):
    same_user = (hexchat.nickcmp(hexchat.get_info("nick").lower(), nick.lower()) == 0)
    hilight = (not same_user and hexchat.get_info("nick").lower() in message.lower())
    if (same_user):
        hexchat.emit_print("Your Message", nick, message, mode, "\00306" + nick_prefix + "\00304")
    elif (hilight):
        hexchat.emit_print("Channel Msg Hilight", nick, message, mode, "\00306" + nick_prefix + "\00303")
    else:
        hexchat.emit_print("Channel Message", nick, message, mode, "\00306" + nick_prefix + "\00302")
    # TODO : Gérer la couleur actuelle du chan
    # hexchat.command("GUI COLOR {}".format("3" if hilight else "2"))

def msg_cmd(word, word_eol, userdata):
    global cmd_nick
    if (hexchat.nickcmp(word[0], bot_nick) == 0):
        # Classic message
        if (len(re.findall(re_msg_format, word[1])) > 0):
            nick, message = re.findall(re_msg_format, word[1])[0]
            nick = hexchat.strip(nick)
            EmitMsg(nick, message, word[2])
            return hexchat.EAT_HEXCHAT
        # Command (part. 1)
        elif (len(re.findall(re_cmd_format, word[1])) > 0):
            cmd_nick = hexchat.strip(re.findall(re_cmd_format, word[1])[0])
            return hexchat.EAT_HEXCHAT
        # Command (part. 2)
        elif (cmd_nick != None and word[1][0] == "!"):
            EmitMsg(cmd_nick, word[1], word[2])
            cmd_nick = None
            return hexchat.EAT_HEXCHAT
        # Someone joined
        elif (len(re.findall(re_join_format, word[1])) > 0):
            nick = nick_prefix + hexchat.strip(re.findall(re_join_format, word[1])[0])
            hexchat.command("RECV :{}!~{}@{} JOIN {}".format(nick, bot_nick, bot_vhost, hexchat.get_info("channel")))
            hexchat.command("RECV :{}!~{}@{} MODE {} +v {}".format(bot_nick, bot_nick, bot_vhost, hexchat.get_info("channel"), nick))
            return hexchat.EAT_HEXCHAT
        # Someone quit
        elif (len(re.findall(re_quit_format, word[1])) > 0):
            nick = nick_prefix + hexchat.strip(re.findall(re_quit_format, word[1])[0])
            hexchat.command("RECV :{}!~{}@{} QUIT {}".format(nick, bot_nick, bot_vhost, quit_message))
            return hexchat.EAT_HEXCHAT
        # Someone change his nick
        elif (len(re.findall(re_rename_format, word[1])) > 0):
            old_nick, new_nick = re.findall(re_rename_format, word[1])[0]
            old_nick = nick_prefix + hexchat.strip(old_nick)
            new_nick = nick_prefix + hexchat.strip(new_nick)
            hexchat.command("RECV :{}!~{}@{} NICK {}".format(old_nick, bot_nick, bot_vhost, new_nick))
            return hexchat.EAT_HEXCHAT
    return hexchat.EAT_NONE

def extbridge_cmd(word, word_eol, userdata):
    if (len(word) < 2):
        hexchat.command("HELP EXTBRIDGE")
    elif (word[1].upper() == "CONF"):
        if (len(word) < 3):
            print("/EXTBRIDGE CONF show|get <name>|set <name> <value>")
        elif (word[2].lower() == "show"):
            print("| {0:<20} | {1:<40} |".format("name", "value"))
            print("|-" + "-"*20 + "-|-" + "-"*40 + "-|")
            for name in hexchat.list_pluginpref():
                print("| {0:<20} | {1:<40} |".format(name, hexchat.get_pluginpref(name)))
        elif (word[2].lower() == "get"):
            if (len(word) < 4):
                print("/EXTBRIDGE CONF get <name>")
            else:
                value = hexchat.get_pluginpref(word[3])
                if (value is None):
                    print("This configuration key doesn't exists.")
                else:
                    print("{} : {}".format(word[3], value))
        elif (word[2].lower() == "set"):
            if (len(word) < 5):
                print("/EXTBRIDGE CONF set <name> <value>")
            else:
                value = hexchat.get_pluginpref(word[3])
                if (value is None):
                    print("This configuration key doesn't exists.")
                else:
                    new_value = hexchat.strip(word_eol[4])
                    hexchat.set_pluginpref(word[3], new_value)
                    LoadPrefs()
                    print("\00307{}\017 has been set to \00307{}\017".format(word[3], new_value))
        else:
            print("Unknown action {} for /EXTBRIDGE CONF".format(word[2]))
    elif (word[1].upper() == "RELOAD"):
        hexchat.command("SETTEXT /PY RELOAD \"{}\"".format(__module_name__))
    else:
        print("Unknown option {} for /EXTBRIDGE".format(word[1]))
    return hexchat.EAT_ALL

def unload(userdata):
    global hooks
    for hook in hooks:
        hexchat.unhook(hook)

hooks = [
    hexchat.hook_print("Channel Message", msg_cmd),
    hexchat.hook_print("Channel Msg Hilight", msg_cmd),
    hexchat.hook_command('EXTBRIDGE', extbridge_cmd, help="/EXTBRIDGE CONF|RELOAD")
]

hexchat.hook_unload(unload)

print("\00307{} v{}\017 : Connected with \00306Discord !".format(__module_name__, __module_version__))