from bs4 import BeautifulSoup as bs 
import cloudscraper
import re
import json
from pprint import pprint
import time
import random

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

MAX_THREADS = 5

# The user will need to populate this list with their own proxies
# Example format: 'http://user:pass@host:port' or 'http://host:port'
PROXIES = [
    'http://190.61.88.147:8080',      # Argentina
    'http://181.129.202.169:8080',    # Paraguay
    'http://138.99.93.42:8080',       # Brazil
    'http://167.250.22.148:8080',     # Brazil
    'http://200.105.215.18:3128',     # Colombia
]

# Create a single, reusable scraper instance
scraper = cloudscraper.create_scraper()

def checkForUpdateGuilds(numberOfIDs, iterator):
    fracturedGuildsURL = 'https://fracturedmmo.com/guild-profile/id/{}'
    allGuilds = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [ executor.submit(fetchAndCollect, fracturedGuildsURL.format(id + ( iterator * numberOfIDs )), id + ( iterator * numberOfIDs )) for id in range(numberOfIDs) ]
    
        for future in as_completed(futures):
            try:
                result = future.result()
                if result is not None:
                    allGuilds.append(result)
            except cloudscraper.exceptions.CloudflareChallengeError as e:
                print(f"Cloudflare challenge failed for a guild, skipping. Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred for a guild, skipping. Error: {e}")

    return allGuilds

def getGuildPage(id):
    fracturedGuildsURL = 'https://fracturedmmo.com/guild-profile/id/{}'
    return fetchAndCollect(fracturedGuildsURL.format(id), id);

def fetchAndCollect(url, id):
    time.sleep(random.uniform(1.0, 2.5)) # Keep the polite delay

    proxy_config = None
    if PROXIES:
        proxy_url = random.choice(PROXIES)
        proxy_config = { 'http': proxy_url, 'https': proxy_url }

    return collectGuildPageData(scraper.get(url, proxies=proxy_config, timeout=15).text, id)

def collectGuildPageData(pageopen, id):
    soup = bs(pageopen,'html.parser')

    # Create json object to store guild
    data = { 'Id' : id }

    # find a predictible section to scope our search to
    profileSection = soup.find(id="profile_displayer")
    
    if not profileSection:
        print(f"Could not find 'profile_displayer' for guild ID {id}. Page structure may have changed.")
        return None

    sectionHeaders = profileSection.findAll(['h1', 'h2', 'h3', 'h4'])

    # if this value equals guildName we have encountered re-direction to default 'Create Guild' page
    if sectionHeaders[0].text == 'Guild Name':
        return None

    data['Name'] = sectionHeaders[0].text

    # Get more significant details - Name, Description, Foundation Points, Guild Master, Lieutenants, Guild Members    
    UniqueHeaders = list(set(sectionHeaders))
    
    for header in UniqueHeaders:

        if header.text == 'LIEUTENANTS':
            valueContents = header.findNext('div').findAll('p')
            textValuesFromContents = []
            for content in valueContents:
                textValuesFromContents.append(content.text)
            key = header.text.title()
            value = textValuesFromContents
            data[key] = textValuesFromContents
            # print(data['Name'], "KEY :: ", key, " || VALUE :: ", value)

        if header.text == 'DESCRIPTION':
            descriptionText = header.parent.p.text
            key = header.text.title()
            value = re.sub(r'(\\r|\\n)+•?', '', descriptionText)
            data[key] = value
            # print("KEY :: ", key, " || VALUE :: ", value)

        if header.text == 'GUILD MEMBERS':
            valueContents = header.findNext('div').findAll('p')
            textValuesFromContents = []
            for content in valueContents:
                textValuesFromContents.append(content.text)
            key = ''.join(x for x in header.text.title() if not x.isspace())
            value = textValuesFromContents
            data[key] = value
            # print(data['Name'], "KEY :: ", key, " || VALUE :: ", value)

        if header.text == 'GUILD MASTER':
            key = ''.join(x for x in header.text.title() if not x.isspace())
            value = header.parent.p.text
            data[key] = value
            # print("KEY :: ", key, " || VALUE :: ", value)

    # collect small descriptions.  see them named below.
    smallDetails = list(filter(None.__ne__, [element.find('b') for element in profileSection.findAll('p')]))

    # Get the upper section basic details - Tag, Race, Master, Members, Total Pts, Avg. Pts.
    smallDetailsText = []
    for detail in smallDetails:
        smallDetailsText.append(detail.parent.text)
    
    for i in range(len(smallDetailsText)):
        key = re.sub(r"\s+", "", smallDetailsText[i].split(':')[0])
        value = re.sub(r"\s+", "", smallDetailsText[i].split(':')[1])
        data[key] = value
    # print("TAG :: ",data['Tag'], " || RACE :: ",data['Race'], " || MASTER :: ",data['Master'])

    # Get the entire HTML for the banner_display div -- we'll clean it up later
    bannerDisplay = soup.find(id="banner_displayer")
    data['bannerDisplayTemplate'] = str(bannerDisplay.div)
    # pprint(bannerDisplay.div)

    json_data = json.dumps(data)
    # pprint(json.loads(json_data)['AveragePoints'])
    return json_data
