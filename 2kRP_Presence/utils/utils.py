import json
import re
import requests
from utils.constants import get_app_version
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

def validate_url(url):
        """
        Validates if the provided URL is valid.
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

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
        # Insert constant replacements that don't change
        replacements.update({
            'version': get_app_version()
        })
        value = replace_patterns(value, replacements)

    return value

def get_image_link(soup, selector):
    img_link = soup.select_one(selector)
    if img_link and img_link['href'].startswith('/File'):
        thumbborder = soup.select_one('img.thumbborder')
        if thumbborder:
            return BASE_WIKI_URL + thumbborder['src']
    return img_link['href'] if img_link else None

def get_wiki_image(wiki_url: str):
    """
    Tries to get the current room image from yume.wiki website.
    Returns: the image source (direct link) or `None`
    """
    if not wiki_url:
        return None

    try:
        response = requests.get(wiki_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error getting wiki page: {e}")
        return None

    selectors = [
        '#tab-content-facts-list > div > div > div.smw-table.smwfacttable > div:nth-child(2) > div.smw-table-cell.smwprops > a',
        '#tab-content-facts-list > div > div > div.smw-table.smwfacttable > div:nth-child(3) > div.smw-table-cell.smwprops > a',
        '#mw-content-text > div > table > tbody > tr:nth-child(2) > td > a > img'
    ]

    for selector in selectors:
        image_url = get_image_link(soup, selector)
        if image_url:
            return BASE_WIKI_URL + image_url if image_url.startswith('/') else image_url

    return None