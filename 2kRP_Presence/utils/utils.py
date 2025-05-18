import json
import re
import requests
from bs4 import BeautifulSoup
from utils.constants import (
    BASE_WIKI_URL,
    DEFAULT_LANGUAGE,
)

_translation_cache = {}

def load_json(file_path: str):
    """Loads a JSON file and returns its content as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}

def replace_patterns(text: str, replacements: dict) -> str:
    """
    Replaces all patterns in the '{pattern}' format by the specified values in the replacements dict.
    
    The patterns are defined as '{key}' and the replacements dict should contain the key-value pairs.
    
    Args:
        text (str): The original string containing the patterns.
        replacements (dict): A dictionary where keys are the patterns to be replaced and values are the replacements.

    Returns:
        str: The string with all patterns replaced.
    """
    def replacer(match):
        key = match.group(1)
        return str(replacements.get(key, match.group(0)))

    return re.sub(r'\{([^}]+)\}', replacer, text)

def validate_url(url: str):
    """Validates if the provided URL is valid."""
    url_pattern = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        r'(/[^\s]*)?'
        r'\.(png|jpg|jpeg|gif|bmp|webp|svg)$',
        re.IGNORECASE
    )

    return bool(url_pattern.match(url))

def load_translation(language_code):
    return load_json(f"langs/{language_code}.json")

def get_translated_string(key: str):
    """Retrieves the translated string for the given key based on the current language setting."""
    with open('language.txt', 'r', encoding='utf-8') as file:
        language = file.read().strip()
    
    if language not in _translation_cache:
        _translation_cache[language] = load_translation(language)
    
    translations = _translation_cache[language]
    if key in translations:
        return translations[key]
    
    if DEFAULT_LANGUAGE != language:
        if DEFAULT_LANGUAGE not in _translation_cache:
            _translation_cache[DEFAULT_LANGUAGE] = load_translation(DEFAULT_LANGUAGE)
        default_translations = _translation_cache[DEFAULT_LANGUAGE]
        return default_translations.get(key, f"'{key}' not found in '{DEFAULT_LANGUAGE}'")
    
    return f"'{key}' not found in '{language}'"

def get_image_link(soup, selector):
    """Extracts the image link from the soup object using the provided selector."""
    img_link = soup.select_one(selector)
    if img_link and img_link['href'].startswith('/File'):
        thumbborder = soup.select_one('img.thumbborder')
        if thumbborder:
            return BASE_WIKI_URL + thumbborder['src']
    return img_link['href'] if img_link else None

def get_wiki_image(wiki_url: str):
    """
    Tries to get the current room image from yume.wiki website.
    
    Returns:
        str: The URL of the image if found, otherwise None.
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