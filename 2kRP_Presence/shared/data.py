class DataStore:
    def __init__(self):
        self._data_store = {
            'gameType': None,
            'location': None,
            'badgeImageUrl': None,
            'playersOnline': '0',
            'playersOnMap': '0',
            'wikiPageUrl': None
        }

    def update_data(self, gameType, location, badgeImageUrl, playersOnline, playersOnMap, wikiPageUrl):
        """Update storage data."""
        self._data_store['gameType'] = gameType
        self._data_store['location'] = location
        self._data_store['badgeImageUrl'] = badgeImageUrl
        self._data_store['playersOnline'] = playersOnline
        self._data_store['playersOnMap'] = playersOnMap
        self._data_store['wikiPageUrl'] = wikiPageUrl

    def get_data(self):
        """Get storage data."""
        return self._data_store

data_store = DataStore()

def update_data(gameType, location, badgeImageUrl, playersOnline, playersOnMap, wikiPageUrl):
    """Global function to update data in store."""
    data_store.update_data(gameType, location, badgeImageUrl, playersOnline, playersOnMap, wikiPageUrl)

def get_data():
    """Global function to retrieve data."""
    return data_store.get_data()