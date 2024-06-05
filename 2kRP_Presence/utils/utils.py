import json
import re

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def replace_patterns(value, replacements):
    """
    Replaces the patterns in the $pattern format for the corresponding value in replacements.
    """
    def replacer(match):
        key = match.group(1)
        return replacements.get(key, match.group(0))
    
    pattern = re.compile(r'\$(\w+)')
    return pattern.sub(replacer, value)

def get_preference(key, replacements=None):
    """
    Returns a configuration value from the preferences file (preferences.json)
    Example: get_config('dream_world')
    Returns: "Dreaming"
    """
    if replacements is None:
        replacements = {}
    
    config = load_json('preferences.json')
    value = config.get(key)
    
    if isinstance(value, str):
        value = replace_patterns(value, replacements)
    
    return value