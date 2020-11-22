from app import app

from database.db import initialize_db

import time, http, scraper, mongostore, requests

from mongoengine import *

app.config['MONGODB_SETTINGS'] = {
    'name': 'guild-discovery',
    'host': 'mongo',
    'port': 27017
}

# connect('')

port = 5000

initialize_db(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)

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
            print('remote failed..')
            guildChunkList = ['continue']
            continue
    
    print('Done!')