import os
import requests
from osgeo import gdal, osr
from fastapi import HTTPException

ACTINIA_URL = "http://localhost:8088/api/v3"
AUTH = ("actinia-gdi", "actinia-gdi")

def get_epsg_from_raster(file_path: str) -> int:
    dataset = gdal.Open(file_path)
    if not dataset:
        raise ValueError("Failed to open raster file with GDAL")

    proj = dataset.GetProjection()
    if not proj:
        raise ValueError("No projection found in raster file")

    srs = osr.SpatialReference(wkt=proj)
    if srs.IsProjected() or srs.IsGeographic():
        epsg = srs.GetAttrValue("AUTHORITY", 1)
        if epsg:
            return int(epsg)
        else:
            raise ValueError("AUTHORITY (EPSG) not found in SRS")
    else:
        raise ValueError("SRS is neither projected nor geographic — no EPSG found")

from osgeo import ogr

def get_epsg_from_vector(file_path: str) -> int:
    ds = ogr.Open(file_path)
    if not ds:
        raise ValueError("Failed to open vector file with OGR")

    layer = ds.GetLayer()
    if not layer:
        raise ValueError("No layers found in vector file")

    sr = layer.GetSpatialRef()
    if not sr:
        raise ValueError("No spatial reference found")

    epsg = sr.GetAttrValue("AUTHORITY", 1)
    if epsg:
        return int(epsg)
    else:
        raise ValueError("No EPSG authority code found")

def create_location_and_mapset(location: str, mapset: str, epsg: int):
    # Check existing locations
    loc_resp = requests.get(f"{ACTINIA_URL}/locations", auth=AUTH)
    if loc_resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch locations from Actinia")

    existing_locations = loc_resp.json().get("projects", [])

    # Create location if not exists
    if location not in existing_locations:
        payload = {"epsg": str(epsg)}
        create_resp = requests.post(f"{ACTINIA_URL}/locations/{location}", json=payload, auth=AUTH)
        if create_resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to create location: {create_resp.text}")

    # Check existing mapsets
    mapset_resp = requests.get(f"{ACTINIA_URL}/locations/{location}/mapsets", auth=AUTH)
    stdout = mapset_resp.json().get("process_log", [])[0].get("stdout", "")
    existing_mapsets = stdout.strip().split()

    # Create mapset if not exists
    if mapset not in existing_mapsets:
        create_mapset_resp = requests.post(f"{ACTINIA_URL}/locations/{location}/mapsets/{mapset}", auth=AUTH)
        if create_mapset_resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to create mapset: {create_mapset_resp.text}")
