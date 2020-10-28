from bs4 import BeautifulSoup as bs 
import requests   # importing requests module to open a URL
import re
import json
from pprint import pprint

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

MAX_THREADS = 25

def checkForUpdateGuilds(numberOfIDs, iterator):
    fracturedGuildsURL = 'https://fracturedmmo.com/guild-profile/id/{}'
    allGuilds = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [ executor.submit(fetchAndCollect, fracturedGuildsURL.format(id + ( iterator * numberOfIDs )), id + ( iterator * numberOfIDs )) for id in range(numberOfIDs) ]
    
        for result in as_completed(futures):
            if result.result() != None:
                allGuilds.append(result.result())

    return allGuilds

def getGuildPage(id):
    fracturedGuildsURL = 'https://fracturedmmo.com/guild-profile/id/{}'
    return fetchAndCollect(fracturedGuildsURL.format(id), id);

def fetchAndCollect(url, id):
    return collectGuildPageData(requests.get(url).text, id)

def collectGuildPageData(pageopen, id):
    soup = bs(pageopen,'html.parser')

    # Create json object to store guild
    data = { 'Id' : id }

    # find a predictible section to scope our search to
    profileSection = soup.find(id="profile_displayer")
    
    sectionHeaders = profileSection.findAll(['h1', 'h2', 'h3', 'h4'])

    # if this value equals guildName we have encountered re-direction to default 'Create Guild' page
    if sectionHeaders[0].text == 'Guild Name':
        return None

    data['Name'] = sectionHeaders[0].text

    # Get more significant details - Name, Description, Foundation Points, Guild Master, Lieutenants, Guild Members    
    UniqueHeaders = list(set(sectionHeaders))
    
    for header in UniqueHeaders:

        if header.text == 'LIEUTENANTS':
            valueContents = header.parent.findAll('p')
            textValuesFromContents = []
            for content in valueContents:
                textValuesFromContents.append(content.text)
            key = header.text.title()
            value = textValuesFromContents
            data[key] = textValuesFromContents
            # print("KEY :: ", key, " || VALUE :: ", value)

        if header.text == 'DESCRIPTION':
            descriptionText = header.parent.p.text
            key = header.text.title()
            value = re.sub(r'(\\r|\\n)+•?', '', descriptionText)
            data[key] = value
            # print("KEY :: ", key, " || VALUE :: ", value)

        if header.text == 'GUILD MEMBERS':
            valueContents = header.parent.findAll('p')
            textValuesFromContents = []
            for content in valueContents:
                textValuesFromContents.append(content.text)
            key = ''.join(x for x in header.text.title() if not x.isspace())
            value = textValuesFromContents
            data[key] = value
            # print("KEY :: ", key, " || VALUE :: ", value)

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
