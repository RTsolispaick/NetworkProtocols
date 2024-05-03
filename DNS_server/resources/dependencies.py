import json


def get_server_settings() -> dict:
    with open("resources/config.json", "r") as jsonfile:
        settings = json.load(jsonfile)
    return settings
