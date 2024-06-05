import time
import os
from pypresence import Presence
from dotenv import load_dotenv
from shared.data import get_data
from utils.utils import get_preference
from color.colors import print_green, print_yellow

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
START_TIME = time.time()

real_world_locations = {'Urotsuki\'s Room',
                        'Urotsuki\'s Balcony',
                        'Sound Room',
                        'Old Sound Room'}

minigames = {'Plated Snow Country',
            'Red Blue Yellow (Mini Game B)',
            'Red Blue Yellow (Mini Game B) - EX Version',
            '↑v↑ (Wavy Up)',
            'Puzzle Game (Kura Puzzle)',
            'Gimmick Runner'}

real_world_image = 'https://i.imgur.com/TN8WK7E.png'
dream_world_image = 'https://i.imgur.com/de3xUvd.png'

def get_presence_data():
    data = get_data()
    location = None
    badge_image_url = None
    players_online = '0'
    players_on_map = '0'
    
    # Will attempt to retrieve location from data
    # If not possible, will halt until location is available
    try:
        location = data['location']
        badge_image_url = data['badgeImageUrl']
        players_online = data['playersOnline']
        players_on_map = data['playersOnMap']
    except Exception:
        return {'state': 'Getting ready...'}
    
    # Default
    details_message = 'Dream World'
    state_message = get_preference('location_text', {'location': location or 'Unknown Location'})
    large_image_url = dream_world_image
    large_image_text = get_preference('large_image_text', {'playersonline': players_online, 'playersonmap': players_on_map})

    # Location filtering
    if location in real_world_locations: # Real World
        details_message = get_preference('real_world_text')
        large_image_url = real_world_image
    elif location in minigames: # Real World
        details_message = get_preference('real_world_text')
        state_message = get_preference('minigame_text')
        large_image_url = real_world_image
    
    presenceState = {'state': state_message,
                     'details': details_message,
                     'large_image': large_image_url,
                     'large_text': large_image_text,
                     'small_image': badge_image_url,
                     'small_text': get_preference('small_image_text'),
                     'start': START_TIME
                     }
    return presenceState

def run_presence(stop_flag):
    presence = Presence(CLIENT_ID)
    
    try:
        presence.connect()
    except Exception as e:
        print_yellow('WARNING: The application returned an exception trying to connect. This is probably due to Discord not being properly detected.')
        print(f'The following exception has been raised: {e}')
        time.sleep(30)
        return
    
    print_green('Connection with client established!')    
    
    while not stop_flag.is_set():
        try:
            data = get_presence_data()
            presence.update(**data)
            time.sleep(15)
        except Exception:
            pass