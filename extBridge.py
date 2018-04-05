import hexchat
import re

__module_name__ = 'External Bridge Adaptor'
__module_version__ = '2.0'
__module_description__ = 'Adapt Hexchat UI for external bridges'
__author__ = 'Stockage'

CONF_PREFIX = "extbridge_"

class Bridge:
    def __init__(self, bot_channel, bot_server, bot_nick, quit_message="Disconnected from discord", nick_prefix="<DSC>", re_msg_format="^<([^>]+)> (.*)$", re_cmd_format="^Cmd by (.+)$"):
        self.bot_channel = bot_channel
        self.bot_server = bot_server
        self.bot_nick = bot_nick
        self.quit_message = quit_message
        self.nick_prefix = nick_prefix
        self.re_msg_format = re_msg_format
        self.re_cmd_format = re_cmd_format
        self.cmd_nick = None
    
    def __str__(self):
        bstr = ""
        for attr in ["bot_channel", "bot_server", "bot_nick", "quit_message", "nick_prefix", "re_msg_format", "re_cmd_format"]:
            bstr += "\00305{}\00308 = \017{}\n".format(attr, getattr(self, attr))
        return bstr
    
    def IsBridgeMessage(self, context, nick):
        if self.bot_server.startswith("*"):
            correct_serv = context.get_info("server").lower().endswith(self.bot_server.lower()[1:])
        else:
            correct_serv = context.get_info("server").lower() == self.bot_server.lower()
        return correct_serv and context.get_info("channel").lower() == self.bot_channel.lower() and hexchat.nickcmp(hexchat.strip(nick), self.bot_nick) == 0
        

def InitPref(name, default_value):
    value = hexchat.get_pluginpref(CONF_PREFIX + name)
    if (value is None):
        value = default_value
        hexchat.set_pluginpref(CONF_PREFIX + name, value)
    return value

def LoadPrefs():
    bridge_count = InitPref("bridge_count", 0)
    for i in range(bridge_count):
        bot_channel = hexchat.get_pluginpref("{}bridge{}_bot_channel".format(CONF_PREFIX, i))
        bot_server = hexchat.get_pluginpref("{}bridge{}_bot_server".format(CONF_PREFIX, i))
        bot_nick = hexchat.get_pluginpref("{}bridge{}_bot_nick".format(CONF_PREFIX, i))
        quit_message = hexchat.get_pluginpref("{}bridge{}_quit_message".format(CONF_PREFIX, i))
        nick_prefix = hexchat.get_pluginpref("{}bridge{}_nick_prefix".format(CONF_PREFIX, i))
        re_msg_format = hexchat.get_pluginpref("{}bridge{}_re_msg_format".format(CONF_PREFIX, i))
        re_cmd_format = hexchat.get_pluginpref("{}bridge{}_re_cmd_format".format(CONF_PREFIX, i))
        bridge_list.append(Bridge(bot_channel, bot_server, bot_nick, quit_message=quit_message, nick_prefix=nick_prefix, re_msg_format=re_msg_format, re_cmd_format=re_cmd_format))

def SavePref():
    bridge_count = hexchat.get_pluginpref(CONF_PREFIX + "bridge_count")
    for i in range(bridge_count):
        hexchat.del_pluginpref("{}bridge{}_bot_channel".format(CONF_PREFIX, i))
        hexchat.del_pluginpref("{}bridge{}_bot_server".format(CONF_PREFIX, i))
        hexchat.del_pluginpref("{}bridge{}_bot_nick".format(CONF_PREFIX, i))
        hexchat.del_pluginpref("{}bridge{}_quit_message".format(CONF_PREFIX, i))
        hexchat.del_pluginpref("{}bridge{}_nick_prefix".format(CONF_PREFIX, i))
        hexchat.del_pluginpref("{}bridge{}_re_msg_format".format(CONF_PREFIX, i))
        hexchat.del_pluginpref("{}bridge{}_re_cmd_format".format(CONF_PREFIX, i))
    hexchat.set_pluginpref(CONF_PREFIX + "bridge_count", len(bridge_list))
    for bridge_index in range(len(bridge_list)):
        bridge = bridge_list[bridge_index]
        hexchat.set_pluginpref("{}bridge{}_bot_channel".format(CONF_PREFIX, bridge_index), bridge.bot_channel)
        hexchat.set_pluginpref("{}bridge{}_bot_server".format(CONF_PREFIX, bridge_index), bridge.bot_server)
        hexchat.set_pluginpref("{}bridge{}_bot_nick".format(CONF_PREFIX, bridge_index), bridge.bot_nick)
        hexchat.set_pluginpref("{}bridge{}_quit_message".format(CONF_PREFIX, bridge_index), bridge.quit_message)
        hexchat.set_pluginpref("{}bridge{}_nick_prefix".format(CONF_PREFIX, bridge_index), bridge.nick_prefix)
        hexchat.set_pluginpref("{}bridge{}_re_msg_format".format(CONF_PREFIX, bridge_index), bridge.re_msg_format)
        hexchat.set_pluginpref("{}bridge{}_re_cmd_format".format(CONF_PREFIX, bridge_index), bridge.re_cmd_format)

bridge_list = []
LoadPrefs()

def EmitMsg(context, nick, message, mode, nick_prefix):
    same_user = (hexchat.nickcmp(hexchat.get_info("nick").lower(), nick.lower()) == 0)
    hilight = (not same_user and hexchat.get_info("nick").lower() in message.lower())
    if same_user:
        context.emit_print("Your Message", nick, message, mode, "\00306" + nick_prefix + "\00304")
    elif hilight:
        context.emit_print("Channel Msg Hilight", nick, message, mode, "\00306" + nick_prefix + "\00303")
    else:
        context.emit_print("Channel Message", nick, message, mode, "\00306" + nick_prefix + "\00302")

def msg_cmd(word, word_eol, userdata):
    context = hexchat.get_context()
    for bridge in bridge_list:
        # Current server/channel
        if bridge.IsBridgeMessage(context, word[0]):
            # Classic message
            if len(re.findall(bridge.re_msg_format, word[1])) > 0:
                nick, message = re.findall(bridge.re_msg_format, word[1])[0]
                nick = hexchat.strip(nick)
                EmitMsg(context, nick, message, word[2] if len(word) > 2 else "", bridge.nick_prefix)
                return hexchat.EAT_HEXCHAT
            # Command (part. 1)
            elif len(re.findall(bridge.re_cmd_format, word[1])) > 0:
                bridge.cmd_nick = hexchat.strip(re.findall(bridge.re_cmd_format, word[1])[0])
                return hexchat.EAT_HEXCHAT
            # Command (part. 2)
            elif bridge.cmd_nick != None and word[1][0] == "!":
                EmitMsg(context, bridge.cmd_nick, word[1], word[2] if len(word) > 2 else "", bridge.nick_prefix)
                bridge.cmd_nick = None
                return hexchat.EAT_HEXCHAT
    return hexchat.EAT_NONE

def extbridge_cmd(word, word_eol, userdata):
    if len(word) < 2:
        hexchat.command("HELP EXTBRIDGE")
    elif word[1].upper() == "BRIDGE":
        if len(word) < 3:
            print("/EXTBRIDGE BRIDGE list|add <channel> <server> <bot_nick>|show <index>|set <index> <prop> <value>|del <index>")
        elif word[2].lower() == "list":
            bridge_count = hexchat.get_pluginpref(CONF_PREFIX + "bridge_count")
            bridge_list_params = []
            params_lens = [1, 6, 7]
            for i in range(bridge_count):
                bot_server = hexchat.get_pluginpref("{}bridge{}_bot_server".format(CONF_PREFIX, i))
                bot_channel = hexchat.get_pluginpref("{}bridge{}_bot_channel".format(CONF_PREFIX, i))
                params_lens[0] = max(params_lens[0], len("{}".format(i)) + 2)
                params_lens[1] = max(params_lens[1], len(bot_server) + 2)
                params_lens[2] = max(params_lens[2], len(bot_channel) + 2)
                bridge_list_params.append((bot_server, bot_channel))
            print(("| {0:<" + str(params_lens[0]) + "} | {1:<" + str(params_lens[1]) + "} | {2:<" + str(params_lens[2]) + "} |").format("#", "server", "channel"))
            print("|-" + "-"*params_lens[0] + "-|-" + "-"*params_lens[1] + "-|-" + "-"*params_lens[2] + "-|")
            for i in range(bridge_count):
                print(("| {0:<" + str(params_lens[0]) + "} | {1:<" + str(params_lens[1]) + "} | {2:<" + str(params_lens[2]) + "} |").format(i, bridge_list_params[i][0], bridge_list_params[i][1]))
        elif word[2].lower() == "add":
            if len(word) < 6:
                context = hexchat.get_context()
                hexchat.command("SETTEXT /EXTBRIDGE BRIDGE add {} {} <bot_nick>".format(context.get_info("channel"), context.get_info("server")))
                hexchat.command("SETCURSOR {}".format(24 + len(context.get_info("channel")) + len(context.get_info("server"))))
            else:
                bridge = Bridge(word[3], word[4], word[5])
                bridge_list.append(bridge)
                SavePref()
                print("Bridge for \00307{}\017 on \00307{}\017 has been set.".format(bridge.bot_channel, bridge.bot_server))
        elif word[2].lower() == "show":
            if len(word) < 4:
                hexchat.command("SETTEXT /EXTBRIDGE BRIDGE show <index>")
                hexchat.command("SETCURSOR 23")
            else:
                try:
                    print(bridge_list[int(word[3])])
                except:
                    print("Bad index value.")
        elif word[2].lower() == "set":
            if len(word) < 6:
                hexchat.command("SETTEXT /EXTBRIDGE BRIDGE set <index> <prop> <value>")
                hexchat.command("SETCURSOR 22")
            else:
                try:
                    setattr(bridge_list[int(word[3])], word[4], word_eol[5])
                    SavePref()
                    print("Parameter \00307{}\017 for bridge \00307N°{}\017 has been changed to \00307{}\017.".format(word[4], word[3], word_eol[5]))
                except:
                    print("Bad index value.")
        elif word[2].lower() == "del":
            if len(word) < 4:
                hexchat.command("SETTEXT /EXTBRIDGE BRIDGE del <index>")
                hexchat.command("SETCURSOR 22")
            else:
                try:
                    del bridge_list[int(word[3])]
                    SavePref()
                    print("Bridge deleted.")
                except:
                    print("Bad index value.")
    elif word[1].upper() == "CONF":
        if len(word) < 3:
            print("/EXTBRIDGE CONF show|get <name>|set <name> <value>")
        elif word[2].lower() == "show":
            print("| {0:<20} | {1:<40} |".format("name", "value"))
            print("|-" + "-"*20 + "-|-" + "-"*40 + "-|")
            for name in hexchat.list_pluginpref():
                if name[:len(CONF_PREFIX)] == CONF_PREFIX:
                    print("| {0:<20} | {1:<40} |".format(name[len(CONF_PREFIX):], hexchat.get_pluginpref(name)))
        elif word[2].lower() == "get":
            if len(word) < 4:
                print("/EXTBRIDGE CONF get <name>")
            else:
                value = hexchat.get_pluginpref(CONF_PREFIX + word[3])
                if value is None:
                    print("This configuration key doesn't exists.")
                else:
                    print("{} : {}".format(word[3], value))
        elif word[2].lower() == "set":
            if len(word) < 5:
                print("/EXTBRIDGE CONF set <name> <value>")
            else:
                value = hexchat.get_pluginpref(CONF_PREFIX + word[3])
                if value is None:
                    print("This configuration key doesn't exists.")
                else:
                    new_value = hexchat.strip(word_eol[4])
                    hexchat.set_pluginpref(CONF_PREFIX + word[3], new_value)
                    LoadPrefs()
                    print("\00307{}\017 has been set to \00307{}\017".format(word[3], new_value))
        else:
            print("Unknown action {} for /EXTBRIDGE CONF".format(word[2]))
    elif word[1].upper() == "RELOAD":
        hexchat.command("SETTEXT /PY RELOAD \"{}\"".format(__module_name__))
    else:
        print("Unknown option {} for /EXTBRIDGE".format(word[1]))
    return hexchat.EAT_ALL

def unload(userdata):
    for hook in hooks:
        hexchat.unhook(hook)

hooks = [
    hexchat.hook_print("Channel Message", msg_cmd),
    hexchat.hook_print("Channel Msg Hilight", msg_cmd),
    hexchat.hook_command('EXTBRIDGE', extbridge_cmd, help="/EXTBRIDGE BRIDGE|CONF|RELOAD")
]

hexchat.hook_unload(unload)

print("\00307{} v{}\017 : Connected with \00306Discord !".format(__module_name__, __module_version__))