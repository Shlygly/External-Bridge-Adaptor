import hexchat
import re

__module_name__ = 'External Bridge Adaptor'
__module_version__ = '1.0'
__module_description__ = 'Adapt Hexchat UI for external bridges'
__author__ = 'Stockage'

bot_nick = "dsc"
re_nick_format = "^:([a-zA-Z0-9_\-\\\[\]{}\^`|]+)!"
re_msg_format = "^:<(.+)> (.+)$"
re_cmd_format = "^:Cmd by (.+):$"

cmd_nick = None

def EmitMsg(nick, message):
    highlight = hexchat.get_info("nick") in message
    hexchat.emit_print("Channel Message", ("\00304" if highlight else "\00302") + nick, ("\00304" if highlight else "") + message, "@", "\00306<DSC>")
    # TODO : Gérer la couleur actuelle du chan
    hexchat.command("GUI COLOR {}".format("3" if highlight else "2"))

def msg_cmd(word, word_eol, userdata):
    global cmd_nick
    emit_nick = re.findall(re_nick_format, word[0])[0]
    if (emit_nick == bot_nick):
        if (cmd_nick != None and word_eol[3][1] == "!"):
            EmitMsg(cmd_nick, word_eol[3][1:])
            cmd_nick = None
            return hexchat.EAT_ALL
        elif (len(re.findall(re_msg_format, word_eol[3])) > 0):
            nick, message = re.findall(re_msg_format, word_eol[3])[0]
            EmitMsg(nick, message)
            return hexchat.EAT_ALL
        elif (len(re.findall(re_cmd_format, word_eol[3])) > 0):
            cmd_nick = re.findall(re_cmd_format, word_eol[3])[0]
            return hexchat.EAT_ALL
    return hexchat.EAT_NONE

hexchat.hook_server("PRIVMSG", msg_cmd)