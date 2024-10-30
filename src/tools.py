import json
from typing import Dict, Any, List

import geopandas as gpd

from fastapi import Request


async def get_client_ip(request: Request) -> str:
    client_ip = request.headers.get("CF-Connecting-IP")

    if not client_ip:
        client_ip = request.headers.get("X-Forwarded-For")

    if not client_ip:
        client_ip = request.client.host

    return client_ip


def frame_to_json(frame: gpd.GeoDataFrame) -> List[Dict[str, Any]]:
    if not frame.size:
        return []

    converted_frame = json.loads(frame.to_json())

    return [feature["properties"] for feature in converted_frame["features"]]
