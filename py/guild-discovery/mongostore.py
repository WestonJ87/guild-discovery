from pprint import pprint

from database.models import Guilds
import json

def updateOrCreateGuild(guildJSON):
    # Returns None or Object if it exists
    jsonDecoded = json.loads(guildJSON)

    result = Guilds.objects(guildID=jsonDecoded['Id'])
    if len(result) == 0:
        newGuild = createGuild(jsonDecoded)
        newGuild.save()
    else:
        pass
        # update guild

def createGuild(jsonDecoded):
    # pprint(json.loads(json_data)['AveragePoints'])
    # print("ID :: ", str(jsonDecoded['Id']), "Name :: ", jsonDecoded['Name'], "Master :: ", jsonDecoded['Master'])
    guild = Guilds( guildID = jsonDecoded['Id'], name = jsonDecoded['Name'], master = jsonDecoded['Master'])
    
    if ('Tag' in jsonDecoded):
        guild.tag = jsonDecoded['Tag']
    if ('Race' in jsonDecoded):
        guild.race = jsonDecoded['Race']
    if ('Members' in jsonDecoded):
        guild.members = jsonDecoded['Members']
    if ('TotalPoints' in jsonDecoded):
        guild.totalPoints = jsonDecoded['TotalPoints']
    if ('AveragePoints' in jsonDecoded):
        guild.avgPoints = jsonDecoded['AveragePoints']
    if ('Description' in jsonDecoded):
        guild.description = jsonDecoded['Description']
    if ('Lieutenants' in jsonDecoded):
        guild.lieutenants = jsonDecoded['Lieutenants']
    
    return guild
    # print()
    # pprint(guild.to_json())

