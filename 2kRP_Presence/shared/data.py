data_store = {
    'gameType': None,
    'location': None,
    'badgeImageUrl': None,
    'playersOnline': '0',
    'playersOnMap': '0',
    'wikiPageUrl': None
}

def update_data(gameType, location, badgeImageUrl, playersOnline, playersOnMap, wikiPageUrl):
    global data_store
    data_store['gameType'] = gameType
    data_store['location'] = location
    data_store['badgeImageUrl'] = badgeImageUrl
    data_store['playersOnline'] = playersOnline
    data_store['playersOnMap'] = playersOnMap
    data_store['wikiPageUrl'] = wikiPageUrl

def get_data():
    global data_store
    return data_store