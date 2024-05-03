import json


def get_server_settings() -> dict:
    with open("C:/Users/User/PycharmProjects/Network_protocols/DNS_server/resources/config.json", "r") as jsonfile:
        settings = json.load(jsonfile)
    return settings
