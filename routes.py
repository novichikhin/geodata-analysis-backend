from typing import Annotated

import pandas as pd
import geopandas as gpd

from fastapi import APIRouter, Depends, Query
from shapely import Point
from starlette import status

from deps import FramesOfObjectsDepsMarker
from models import ObjectModel
from tools import get_client_ip, frame_to_json

router_object = APIRouter()


@router_object.get("/")
async def get_objects(
    frames_of_objects: Annotated[gpd.GeoDataFrame, Depends(FramesOfObjectsDepsMarker)],
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    return frame_to_json(frames_of_objects[client_ip])


@router_object.post("/")
async def create_object(
    new_object: ObjectModel,
    frames_of_objects: Annotated[gpd.GeoDataFrame, Depends(FramesOfObjectsDepsMarker)],
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    new_frame = gpd.GeoDataFrame(
        {
            "name": [new_object.name],
            "latitude": [new_object.latitude],
            "longitude": [new_object.longitude],
        },
        geometry=[Point(new_object.longitude, new_object.latitude)],
        crs="EPSG:4326",
    )

    frames_of_objects[client_ip] = pd.concat([frames_of_objects[client_ip], new_frame])

    return frame_to_json(frames_of_objects[client_ip])


@router_object.post("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_objects(
    frames_of_objects: Annotated[gpd.GeoDataFrame, Depends(FramesOfObjectsDepsMarker)],
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    frames_of_objects[client_ip] = gpd.GeoDataFrame()


@router_object.get("/near")
async def get_near_objects(
    latitude: Annotated[float, Query()],
    longitude: Annotated[float, Query()],
    distance: Annotated[float, Query()],
    frames_of_objects: Annotated[gpd.GeoDataFrame, Depends(FramesOfObjectsDepsMarker)],
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    current_location_frame = gpd.GeoDataFrame(
        geometry=[Point(longitude, latitude)], crs="EPSG:4326"
    )
    current_location_frame = current_location_frame.to_crs(epsg=3857)

    client_frame = frames_of_objects[client_ip]

    if not client_frame.size:
        return []

    client_frame = client_frame.to_crs(epsg=3857)

    distance_series = client_frame.distance(current_location_frame.geometry[0])

    near_objects = client_frame[distance_series <= distance]

    return frame_to_json(near_objects)
