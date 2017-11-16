import hexchat
import re

__module_name__ = 'External Bridge Adaptor'
__module_version__ = '1.0'
__module_description__ = 'Adapt Hexchat UI for external bridges'
__author__ = 'Stockage'

bot_nick = "dsc"
bot_vhost = "discord.newbiecontest.org"
quit_message = "Disconnected from discord"
re_msg_format = "^<([^>]+)> (.+)$"
re_cmd_format = "^Cmd by (.+)$"
re_join_format = "^(.+) has joined$"
re_quit_format = "^(.+) has quit$"
re_rename_format = "^(.+) is now known as (.+)$"

cmd_nick = None

def EmitMsg(nick, message, mode):
    hilight = hexchat.get_info("nick") in message
    hexchat.emit_print("Channel Msg Hilight" if hilight else "Channel Message", nick, message, mode, "\00306<DSC>" + ("\00303" if hilight else "\00302"))
    # TODO : Gérer la couleur actuelle du chan
    hexchat.command("GUI COLOR {}".format("3" if hilight else "2"))

def msg_cmd(word, word_eol, userdata):
    global cmd_nick
    if (hexchat.nickcmp(word[0], bot_nick) == 0):
        # Classic message
        if (len(re.findall(re_msg_format, word[1])) > 0):
            nick, message = re.findall(re_msg_format, word[1])[0]
            EmitMsg(nick, message, word[2])
            return hexchat.EAT_HEXCHAT
        # Command (part. 1)
        elif (len(re.findall(re_cmd_format, word[1])) > 0):
            cmd_nick = re.findall(re_cmd_format, word[1])[0]
            return hexchat.EAT_HEXCHAT
        # Command (part. 2)
        elif (cmd_nick != None and word[1][0] == "!"):
            EmitMsg(cmd_nick, word[1], word[2])
            cmd_nick = None
            return hexchat.EAT_HEXCHAT
        # Someone joined
        elif (len(re.findall(re_join_format, word[1])) > 0):
            nick = re.findall(re_join_format, word[1])[0]
            hexchat.command("RECV :{}!~{}@{} JOIN {}".format(nick, bot_nick, bot_vhost, hexchat.get_info("channel")))
            return hexchat.EAT_HEXCHAT
        # Someone quit
        elif (len(re.findall(re_quit_format, word[1])) > 0):
            nick = re.findall(re_quit_format, word[1])[0]
            hexchat.command("RECV :{}!~{}@{} QUIT {}".format(nick, bot_nick, bot_vhost, quit_message))
            return hexchat.EAT_HEXCHAT
        # Someone change his nick
        elif (len(re.findall(re_rename_format, word[1])) > 0):
            old_nick, new_nick = re.findall(re_rename_format, word[1])[0]
            hexchat.command("RECV :{}!~{}@{} NICK {}".format(old_nick, bot_nick, bot_vhost, new_nick))
            return hexchat.EAT_HEXCHAT
    return hexchat.EAT_NONE

    
def unload(userdata):
    for hook in hooks:
        hexchat.unhook(hook)

hooks = [
    hexchat.hook_print("Channel Message", msg_cmd),
    hexchat.hook_print("Channel Msg Hilight", msg_cmd)
]

hexchat.hook_unload(unload)