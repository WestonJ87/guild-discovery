from app import app

from database.db import initialize_db
from database.models import Guilds

import time, http, scraper, mongostore, requests, json

from mongoengine import *

app.config['MONGODB_SETTINGS'] = {
    'name': 'guild-discovery',
    'host': 'mongo',
    'port': 27017
}

initialize_db(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

@app.cli.command()
def devRefresh():
    """(Dev Only) Clears and populates the database from a local JSON file."""
    print("Clearing existing guild data...")
    Guilds.objects().delete() # Make sure the collection is empty
    print("Populating database from guild_data.json...")
    with open('guild_data.json') as f:
        guild_data = json.load(f)
        for guild_json in guild_data:
            # The scraper returns JSON strings, so we mimic that
            mongostore.updateOrCreateGuild(json.dumps(guild_json))
    print(f"Successfully stored {len(guild_data)} guilds from local file.")

@app.cli.command()
def refreshGuilds():
    """refresh the guilds on fractured.com to the database."""
    guildChunkList = ['start']
    iterator = 0
    maximumGuildRange = 5000

    while len(guildChunkList) != 0:

        try:
            guildChunkList = []
            # ------------------------------ SCRAPE FRACTURED.COM ----------------------------- #
            print(f'Scraping guilds (set: {iterator})... ', end = '')
            
            # Set chunk size to catch failures faster
            guildsPerChunk = 100

            # Prepare to scrap and set a timer.  Timer is to track how long scrape chunks take
            timeStart = time.time()
            guildChunkList = scraper.checkForUpdateGuilds(guildsPerChunk, iterator)
            timeFinish = time.time()

            # Output time for the chunk and the iterator to represent the set
            print(f"{timeFinish-timeStart} seconds to download { len(guildChunkList) } guilds.")

            # -------------------------------- STORE IN MONGO ----------------------------- #
            if(len(guildChunkList) != 0):
                for guild in guildChunkList:
                    mongostore.updateOrCreateGuild(guild)

            print(f'{len(guildChunkList)} Guilds stored (set: { iterator }): { str(iterator * guildsPerChunk) + " - " + str((iterator + 1) * guildsPerChunk) } in mongodb...')
            
            # -------------------------------------------------------------------------------- #

            # INCREMENT the iterator!
            iterator += 1

            if (len(guildChunkList) == 0 and (iterator * guildsPerChunk) < maximumGuildRange):
                guildChunkList = ['continue']
                continue 
            
        except requests.exceptions.ConnectionError:
            print(f'Connection error on set {iterator}, moving to next set...')
            iterator += 1
            guildChunkList = ['continue']
            continue
    
    print('Done!')