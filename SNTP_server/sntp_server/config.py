import json


def get_server_config() -> dict:
    with open("SNTP_server/config.json", "r") as jsonfile:
        settings = json.load(jsonfile)
    return settings
