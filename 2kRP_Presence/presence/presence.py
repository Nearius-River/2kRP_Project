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

# Defaults
PLACEHOLDER_IMAGE = 'https://i.imgur.com/TN8WK7E.png'
HUB_IMAGE = 'https://static.wikia.nocookie.net/yumenikki/images/9/9c/The_Nexus.png/revision/latest?cb=20110725075611'

game_type_mappings = {
    '2kki': 'Yume 2kki',
    'amillusion': 'Amillusion',
    'braingirl': 'Braingirl',
    'deepdreams': 'Deep Dreams',
    'flow': '.flow',
    'genie': 'Dream Genie',
    'mikan': 'Mikan Muzou',
    'muma': 'Muma Rope',
    'nostalgic': 'nostAlgic',
    'oversomnia': 'Oversomnia',
    'prayers': 'Answered Prayers',
    'sheawaits': 'She Awaits',
    'someday': 'Someday',
    'tsushin': 'Yume Tsushin',
    'unconscious': 'Collective Unconscious',
    'ultraviolet': 'Ultra Violet',
    'unevendream': 'Uneven Dream',
    'yume': 'Yume Nikki'
}

def get_plural_suffix(count):
    return '' if count == 1 else 's'

def format_player_count(player_count, entity='Player'):
    suffix = get_plural_suffix(player_count)
    return f"{player_count} {entity}{suffix}"

def fetch_presence_data():
    """
    Fetches the current presence data from the game.
    
    Returns:
        dict: A dictionary with the presence data.
    """
    data = get_data()
    try:
        game_type = data['gameType']
        location = data['location']
        badge_image_url = data['badgeImageUrl']
        players_online = data['playersOnline']
        players_on_map = data['playersOnMap']
        wiki_page_url = data['wikiPageUrl']
    except KeyError:
        return {'state': 'Loading game...'}
    
    if game_type is None:
        return {'state': 'Picking a game...', 'large_image': HUB_IMAGE}
    
    game_type_full = game_type_mappings.get(game_type, game_type)

    default_replacements = {
        'location': location or 'Unknown Location',
        'playersonline': format_player_count(int(players_online)),
        'playersonmap': format_player_count(int(players_on_map)),
        'gametype': game_type_full
    }
    
    # Define presence text
    details_message = get_preference('details_text', default_replacements)
    state_message = get_preference('state_text', default_replacements)
    large_image_text = get_preference('large_image_text', default_replacements)
    small_image_url = badge_image_url
    
    # Configure large image url
    large_image_option = get_preference('large_image_option')
    if large_image_option == '1': # Use current room image
        wiki_image = get_wiki_image(wiki_page_url)
        large_image_url = wiki_image if wiki_image else PLACEHOLDER_IMAGE
    elif large_image_option == '2': # Use badge image
        large_image_url = badge_image_url or PLACEHOLDER_IMAGE
    else: # Custom image
        large_image_url = get_preference('large_custom_image_url')
        
    # Configure small image url
    small_image_option = get_preference('small_image_option')
    if small_image_option == '1': # Use current room image
        wiki_image = get_wiki_image(wiki_page_url)
        small_image_url = wiki_image if wiki_image else PLACEHOLDER_IMAGE
    elif small_image_option == '2': # Use badge image
        small_image_url = badge_image_url or PLACEHOLDER_IMAGE
    else: # Custom image
        small_image_url = get_preference('small_custom_image_url')

    return {
        'details': details_message,
        'state': state_message,
        'large_image': large_image_url,
        'large_text': large_image_text,
        'small_image': small_image_url,
        'small_text': get_preference('small_image_text', default_replacements),
        'start': START_TIME
    }

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

    previous_state = None

    while not stop_flag.is_set():
        try:
            current_state = fetch_presence_data()
            if current_state != previous_state:
                presence.update(**current_state)
                previous_state = current_state
            time.sleep(15)
        except Exception as e:
            print_yellow(f'An error occurred during presence update: {e}')
            time.sleep(15)
    
    print('Presence ended.')
    presence.clear()
    presence.close()
    exit(0)