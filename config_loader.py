# It loads the config.json and exposes the configuration as a dictionary.
import json
import os

def load_config(config_path='Config/config.json'):
    """
    Loads the configuration from a JSON file.
    
    Args:
        config_path (str): The path to the configuration file.
        
    Returns:
        dict: The configuration data as a dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    return config

