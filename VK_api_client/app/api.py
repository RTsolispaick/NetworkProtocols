from typing import Iterator, Dict, Optional
from urllib import parse

import requests
from app.data import *
from app.dependecies import *

settings = get_server_settings()

def get_user_info(user_id: str) -> Optional[Iterator[UserInfo]]:
    response = _get_response(
        "users.get", user_id, fields="first_name,last_name,sex,bdate,city"
    )

    if "response" in response and len(response["response"]) > 0:
        info = response["response"][0]

        yield UserInfo(
            first_name=info.get("first_name", DEFAULT_FIELD),
            last_name=info.get("last_name", DEFAULT_FIELD),
            bdate=info.get("bdate", DEFAULT_FIELD),
            sex=sex_mapper[info.get("sex", DEFAULT_FIELD)],
            city=info.get("city", {"title": DEFAULT_FIELD}).get("title", DEFAULT_FIELD),
        )


def get_user_friends(
    user_id: str, count: Optional[int] = None
) -> Optional[Iterator[FriendInfo]]:
    params = {"order": "hints", "fields": "first_name,last_name,sex"}

    if count is not None:
        params["count"] = count

    response = _get_response("friends.get", user_id, **params)

    if "response" in response and "items" in response["response"]:
        infos = response["response"]["items"]

        for info in infos:
            yield FriendInfo(
                first_name=info.get("first_name", DEFAULT_FIELD),
                last_name=info.get("last_name", DEFAULT_FIELD),
                sex=sex_mapper[info.get("sex", DEFAULT_FIELD)],
            )


def get_user_albums(
    user_id: str, count: Optional[int] = None
) -> Optional[Iterator[AlbumInfo]]:
    params = dict()

    if count is not None:
        params["count"] = count

    response = _get_response("photos.getAlbums", user_id, **params)

    if "response" in response and "items" in response["response"]:
        infos = response["response"]["items"]

        for info in infos:
            yield AlbumInfo(
                id=info.get("id", DEFAULT_FIELD),
                title=info.get("title", DEFAULT_FIELD),
                description=info.get("description", DEFAULT_FIELD),
                size=info.get("size", DEFAULT_FIELD),
            )


def _get_method_url(method: str, **params) -> str:
    return f"{settings['vk_api_url']}{method}?{parse.urlencode(params)}"


def _get_response(method: str, user_id: str, **kwargs) -> Dict:
    url = _get_method_url(
        method=method,
        user_id=user_id,
        access_token=settings["access_token"],
        v=settings["vk_api_version"],
        **kwargs,
    )

    response = requests.get(url).json()

    if "error" in response and "error_msg" in response["error"]:
        error_msg = response["error"]["error_msg"]
        raise Exception(error_msg)

    return response
