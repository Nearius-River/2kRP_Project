import json
import re
import requests
from bs4 import BeautifulSoup

BASE_WIKI_URL = 'https://yume.wiki'

def load_json(file_path: str):
    """
    Loads JSON data from a file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}

def replace_patterns(value: str, replacements: dict):
    """
    Replaces the patterns in the $pattern format for the corresponding value in replacements.
    """
    def replacer(match):
        key = match.group(1)
        return replacements.get(key, match.group(0))

    pattern = re.compile(r'\$(\w+)')
    return pattern.sub(replacer, value)

def get_preference(key: str, replacements: dict = None):
    """
    Returns a preference value from the preferences file (preferences.json)
    Example: get_preference('dream_world')
    Returns: "Dreaming"
    """
    if replacements is None:
        replacements = {}

    config = load_json('preferences.json')
    value = config.get(key)

    if isinstance(value, str):
        value = replace_patterns(value, replacements)

    return value

def get_wiki_image(wiki_url: str):
    """
    Tries to get the current room image from yume.wiki website.
    Returns: the image source (direct link) or `None`
    """
    if wiki_url is None:
        return None

    try:
        response = requests.get(wiki_url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error getting wiki page: {e}")
        return None

    img_link = soup.select_one('#tab-content-facts-list > div > div > div.smw-table.smwfacttable > div:nth-child(2) > div.smw-table-cell.smwprops > a')

    # Assumes the fact list does not include the "contributing author" field
    if img_link:
        return img_link['href']
    else:
        # Assumes the fact list has the "contributing author" field and tries to get from child 3 instead of 2
        img_link = soup.select_one('#tab-content-facts-list > div > div > div.smw-table.smwfacttable > div:nth-child(3) > div.smw-table-cell.smwprops > a')
        if img_link:
            return img_link['href']
        else:
            # If all else fails, tries to get image from page thumb instead
            img_link = soup.select_one('#mw-content-text > div > table > tbody > tr:nth-child(2) > td > a > img')
            if img_link:
                return BASE_WIKI_URL + img_link['src']

    return None