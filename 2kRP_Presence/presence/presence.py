import time
import os
import sys
from pypresence import Presence
from dotenv import load_dotenv
from shared.data import get_data

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
    location = ''
    
    # Will attempt to retrieve location from data
    # If not possible, will halt until location is available
    try:
        location = data['location']
    except Exception:
        return {'state': 'Getting ready...'}

    # Default
    details_message = 'Dream World'
    state_message = 'In: ' + (location or 'Unknown location')
    large_image_url = dream_world_image

    # Location filtering
    if location == None:
        location = 'Unknown location'
    elif location in real_world_locations:
        details_message = 'Real World'
        large_image_url = real_world_image
    elif location in minigames:
        details_message = 'Real World'
        state_message = 'Playing a minigame'
        large_image_url = real_world_image

    presenceState = {'state': state_message,
                     'details': details_message,
                     'large_image': large_image_url,
                     'large_text': '2kRP by @altdoov',
                     'start': START_TIME
                     }
    return presenceState

def run_presence(stop_flag):
    presence = Presence(CLIENT_ID)
    retries = 0
    max_retries = 3
    
    while retries < max_retries:
        retries += 1
        try:
            presence.connect()
        except Exception as e:
            print('WARNING: No Discord client detected! Be sure you have Discord (desktop app) opened and try again.\nReattempting connection in 30 seconds...')
            time.sleep(30)
            continue
    
    if retries == max_retries:
        print(f'Connection reattemped {max_retries} times without success. Terminating program...')
        time.sleep(5)
        sys.exit(0)
    
    print('Connection established!')    
    
    while not stop_flag.is_set():
        try:
            data = get_presence_data()
            presence.update(**data)
            time.sleep(15)
        except Exception:
            pass