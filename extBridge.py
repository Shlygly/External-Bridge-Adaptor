import hexchat
import re

__module_name__ = 'External Bridge Adaptor'
__module_version__ = '1.0'
__module_description__ = 'Adapt Hexchat UI for external bridges'
__author__ = 'Stockage'

bot_nick = "dsc"
re_msg_format = "^<(.+)> (.+)$"
re_cmd_format = "^Cmd by (.+)$"

cmd_nick = None

def EmitMsg(nick, message):
    hilight = hexchat.get_info("nick") in message
    hexchat.emit_print("Channel Message", ("\00304" if hilight else "\00302") + nick, ("\00304" if hilight else "") + message, "@", "\00306<DSC>")
    # TODO : Gérer la couleur actuelle du chan
    hexchat.command("GUI COLOR {}".format("3" if hilight else "2"))

def msg_cmd(word, word_eol, userdata):
    global cmd_nick
    if (hexchat.nickcmp(word[0], bot_nick) == 0):
        if (cmd_nick != None and word[1][0] == "!"):
            EmitMsg(cmd_nick, word[1])
            cmd_nick = None
            return hexchat.EAT_HEXCHAT
        elif (len(re.findall(re_msg_format, word[1])) > 0):
            nick, message = re.findall(re_msg_format, word[1])[0]
            EmitMsg(nick, message)
            return hexchat.EAT_HEXCHAT
        elif (len(re.findall(re_cmd_format, word[1])) > 0):
            cmd_nick = re.findall(re_cmd_format, word[1])[0]
            return hexchat.EAT_HEXCHAT
    return hexchat.EAT_NONE

    
def unload(userdata):
    for hook in hooks:
        hexchat.unhook(hook)

hooks = [
    hexchat.hook_print("Channel Message", msg_cmd),
    hexchat.hook_print("Channel Msg hilight", msg_cmd)
]

hexchat.hook_unload(unload)