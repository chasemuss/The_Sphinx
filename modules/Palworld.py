import os
import discord

# region [Palworld Bot]
def Palworld(message):
    def is_server_online(hostname='73.155.108.62'): return os.system('ping -c 4 ' + hostname) == 0
    if 'server' in str(message.content).lower(): return 'Server is online!' if is_server_online() else 'Server is offline...'
    if ' type' in str(message.content).lower(): return discord.File('Palworld_Type_Chart.png')
# endregion