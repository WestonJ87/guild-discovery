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
        guild.members = int(jsonDecoded['Members'].replace(',', ''))
    if ('TotalPoints' in jsonDecoded):
        if (jsonDecoded['TotalPoints'] == "--"):
            totalPoints = 0
        else:
            totalPoints = int(jsonDecoded['TotalPoints'].replace(',', ''))  
        guild.totalPoints = totalPoints
    if ('AveragePoints' in jsonDecoded):
        if (jsonDecoded['AveragePoints'] == "--"):
            averagePoints = 0
        else:
            averagePoints = int(jsonDecoded['AveragePoints'].replace(',', ''))
        guild.avgPoints = averagePoints
    if ('Description' in jsonDecoded):
        guild.description = jsonDecoded['Description']
    if ('Lieutenants' in jsonDecoded):
        guild.lieutenants = jsonDecoded['Lieutenants']
    
    return guild
    # print()
    # pprint(guild.to_json())

