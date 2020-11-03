from pprint import pprint

from database.models import Guilds
import json
import random

def getCorrelationsForUser(allGuilds, userInfo):
    guildCorrelationList = []
    for guild in allGuilds:
        guildCorrelationList.append({ "guildID": guild.guildID, "correlationForUser": random.randint(0,100) })
    return guildCorrelationList