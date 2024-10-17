import time
from pypresence import Presence
from shared.data import get_data
from utils.utils import get_presence_preference, get_wiki_image, get_translated_string
from color.colors import print_green, print_yellow

CLIENT_ID = '1246902701535793324'
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
    'if': 'If',
    'mikan': 'Mikan Muzou',
    'muma': 'Muma Rope',
    'nostalgic': 'nostAlgic',
    'oneshot': 'Oneshot',
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
        game_type = data['game_type']
        location = data['location']
        badge_image_url = data['badge_image_url']
        players_online = data['players_online']
        players_on_map = data['players_on_map']
        wiki_page_url = data['wiki_page_url']
    except KeyError:
        return {'state': get_translated_string('presence_loading_game')}
    
    if game_type is None:
        return {'state': get_translated_string('presence_picking_game'), 'large_image': HUB_IMAGE}
    
    game_type_full = game_type_mappings.get(game_type, game_type)

    default_replacements = {
        'location': location or get_translated_string('presence_no_location'),
        'playersonline': format_player_count(players_online),
        'playersonmap': format_player_count(players_on_map),
        'gametype': game_type_full
    }
    
    # Define presence text
    details_message = get_presence_preference('details_text', default_replacements)
    state_message = get_presence_preference('state_text', default_replacements)
    large_image_text = get_presence_preference('large_image_text', default_replacements)
    small_image_url = badge_image_url
    
    # Configure large image url
    large_image_option = get_presence_preference('large_image_option')
    if large_image_option == '1': # Use current room image
        wiki_image = get_wiki_image(wiki_page_url)
        large_image_url = wiki_image if wiki_image else PLACEHOLDER_IMAGE
    elif large_image_option == '2': # Use badge image
        large_image_url = badge_image_url or PLACEHOLDER_IMAGE
    else: # Custom image
        large_image_url = get_presence_preference('large_custom_image_url')
        
    # Configure small image url
    small_image_option = get_presence_preference('small_image_option')
    if small_image_option == '1': # Use current room image
        wiki_image = get_wiki_image(wiki_page_url)
        small_image_url = wiki_image if wiki_image else PLACEHOLDER_IMAGE
    elif small_image_option == '2': # Use badge image
        small_image_url = badge_image_url or PLACEHOLDER_IMAGE
    else: # Custom image
        small_image_url = get_presence_preference('small_custom_image_url')
    
    return {
        'details': details_message,
        'state': state_message,
        'large_image': large_image_url,
        'large_text': large_image_text,
        'small_image': small_image_url,
        'small_text': get_presence_preference('small_image_text', default_replacements),
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
        print_green(get_translated_string('client_connected'))
    except Exception as e:
        print_yellow(get_translated_string('client_connected_exception'), e)
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
            print_yellow(get_translated_string('client_update_exception'), e)
            time.sleep(15)
    
    print(get_translated_string('client_disconnect'))
    presence.clear()
    presence.close()
    exit(0)