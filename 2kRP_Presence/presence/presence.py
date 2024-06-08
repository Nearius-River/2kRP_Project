import time
import os
from pypresence import Presence
from dotenv import load_dotenv
from shared.data import get_data
from utils.utils import get_preference, get_wiki_image
from color.colors import print_green, print_yellow

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
START_TIME = time.time()

# Define locations and images
REAL_WORLD_LOCATIONS = {
    "Urotsuki's Room",
    "Urotsuki's Balcony",
    "Sound Room",
    "Old Sound Room"
}

MINIGAMES = {
    'Plated Snow Country',
    'Red Blue Yellow (Mini Game B)',
    'Red Blue Yellow (Mini Game B) - EX Version',
    '↑v↑ (Wavy Up)',
    'Puzzle Game (Kura Puzzle)',
    'Gimmick Runner'
}

REAL_WORLD_IMAGE = 'https://i.imgur.com/TN8WK7E.png'
DREAM_WORLD_IMAGE = 'https://i.imgur.com/de3xUvd.png'
BASE_WIKI_URL = 'https://yume.wiki'

def get_presence_data():
    """
    Retrieve presence data for Discord rich presence.

    Returns:
        dict: A dictionary with the presence data.
    """
    data = get_data()
    try:
        location = data['location']
        badge_image_url = data['badgeImageUrl']
        players_online = data['playersOnline']
        players_on_map = data['playersOnMap']
        wikiPageUrl = data['wikiPageUrl']
    except KeyError:
        return {'state': 'Getting ready...'}
    
    DEFAULT_REPLACEMENTS = {
        'location': location or 'Unknown Location',
        'playersonline': players_online,
        'playersonmap': players_on_map
    }
    
    # Default messages and images
    details_message = get_preference('dream_world_text', DEFAULT_REPLACEMENTS)
    state_message = get_preference('location_text', DEFAULT_REPLACEMENTS)
    large_image_url = DREAM_WORLD_IMAGE
    large_image_text = get_preference('large_image_text', DEFAULT_REPLACEMENTS)

    # Location filtering while in real world
    if location in REAL_WORLD_LOCATIONS:
        details_message = get_preference('real_world_text', DEFAULT_REPLACEMENTS)
        large_image_url = REAL_WORLD_IMAGE
    elif location in MINIGAMES:
        details_message = get_preference('real_world_text', DEFAULT_REPLACEMENTS)
        state_message = get_preference('minigame_text', DEFAULT_REPLACEMENTS)
        large_image_url = REAL_WORLD_IMAGE

    # Tries to get wiki image
    wiki_image = get_wiki_image(wikiPageUrl)
    if wiki_image:
        large_image_url = wiki_image

    presence_state = {
        'details': details_message,
        'state': state_message,
        'large_image': large_image_url,
        'large_text': large_image_text,
        'small_image': badge_image_url,
        'small_text': get_preference('small_image_text', DEFAULT_REPLACEMENTS),
        'start': START_TIME
    }
    return presence_state

def run_presence(stop_flag):
    """
    Run the presence update loop.

    Args:
        stop_flag (threading.Event): Event to signal when to stop the loop.
    """
    presence = Presence(CLIENT_ID)
    try:
        presence.connect()
        print_green('Connection with Discord client established!')
    except Exception as e:
        print_yellow('WARNING: The application returned an exception trying to connect. This is probably due to Discord not being properly detected.')
        print(f'The following exception has been raised: {e}')
        time.sleep(30)
        return
    
    while not stop_flag.is_set():
        try:
            data = get_presence_data()
            presence.update(**data)
            time.sleep(15)
        except Exception as e:
            print_yellow(f'An error occurred during presence update: {e}')
            time.sleep(15)
    
    print('Presence ended.')
    presence.clear()
    presence.close()