class DataStore:
    def __init__(self):
        self._data_store = {
            'game_type': None,
            'location': None,
            'badge_image_url': None,
            'players_online': 0,
            'players_on_map': 0,
            'wiki_page_url': None
        }

    def update_data(self, game_type: str, location: str, badge_image_url: str, players_online: int, players_on_map: int, wiki_page_url: str):
        """Update storage data."""
        self._data_store['game_type'] = game_type
        self._data_store['location'] = location
        self._data_store['badge_image_url'] = badge_image_url
        self._data_store['players_online'] = players_online
        self._data_store['players_on_map'] = players_on_map
        self._data_store['wiki_page_url'] = wiki_page_url

    def get_data(self):
        """Get storage data."""
        return self._data_store

data_store = DataStore()

def update_data(game_type: str, location: str, badge_image_url: str, players_online: int, players_on_map: int, wiki_page_url: str):
    """Global function to update data in store."""
    data_store.update_data(game_type, location, badge_image_url, players_online, players_on_map, wiki_page_url)

def get_data():
    """Global function to retrieve data."""
    return data_store.get_data()