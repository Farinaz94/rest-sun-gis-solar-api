import geopandas as gpd
import os
import math
from shapely.geometry import Polygon, MultiPolygon
from pathlib import Path  

POSSIBLE_HEIGHT_FIELDS = ['height', 'HEIGHT', 'Height', 'h', 'H', 'ALTEZZA_VO', 'building_h']
POSSIBLE_SLOPE_FIELDS = ['slope', 'SLOPE', 'Slope']


def detect_field(gdf, possible_fields):
    for field in possible_fields:
        if field in gdf.columns:
            return field
    raise ValueError(f"No matching field found in {possible_fields}")


def load_and_standardize_buildings(path: str) -> gpd.GeoDataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    gdf = gpd.read_file(path)

    height_field = detect_field(gdf, POSSIBLE_HEIGHT_FIELDS)
    slope_field = detect_field(gdf, POSSIBLE_SLOPE_FIELDS)

    gdf = gdf[[height_field, slope_field, 'geometry']].copy()
    gdf = gdf.rename(columns={height_field: 'height', slope_field: 'slope'})

    # Reproject to UTM 32N only if it's in degrees 
    if gdf.crs and not gdf.crs.is_projected:
        gdf = gdf.to_crs(epsg=32632)

    return gdf


def generate_inward_buffers(geometry: Polygon, base_height: float, slope_degrees: float, step=0.5, min_area=1.0):
    buffers = []
    distance = step
    slope = math.tan(math.radians(slope_degrees))

    while True:
        inner = geometry.buffer(-distance)
        if inner.is_empty or inner.area < min_area:
            break

        if isinstance(inner, MultiPolygon):
            inner = max(inner.geoms, key=lambda p: p.area)
        elif not isinstance(inner, Polygon):
            break

        height = max(base_height - (slope * distance), 0)
        buffers.append({
            "geometry": inner,
            "height": height,
            "distance": round(distance, 2)
        })
        distance += step

    return buffers


def process_buildings_with_buffers(
    input_path: str,
    base_dir: Path,
    username: str,
    location: str,
    mapset: str
):
    gdf = load_and_standardize_buildings(input_path)
    records = []

    for idx, row in gdf.iterrows():
        print(f"Processing building index: {idx}")

        try:
            geom = row.geometry
            base_height = row.height
            slope_deg = row.slope

            print(f" - Geometry type: {geom.geom_type}, Height: {base_height}, Slope: {slope_deg}")

            rings = generate_inward_buffers(geom, base_height, slope_deg)
            print(f" - Rings generated: {len(rings)}")

            for ring in rings:
                records.append({
                    "geometry": ring["geometry"],
                    "building_id": idx,
                    "height": ring["height"],
                    "distance": ring["distance"]
                })

        except Exception as e:
            print(f"Error on building {idx}: {str(e)}")
            continue

    buffer_gdf = gpd.GeoDataFrame(records, geometry="geometry", crs=gdf.crs)

    # DYNAMIC SAVE PATH
    output_dir = base_dir / "data" / "actinia-data" / "userdata" / username / location / mapset / "buffer"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save each distance group as a GeoJSON
    for dist, group in buffer_gdf.groupby("distance"):
        filename = f"buffer_{str(dist).replace('.', '_')}.geojson"
        output_path = output_dir / filename
        print(f"Saving: {output_path}")
        group.to_file(output_path, driver="GeoJSON")

    return buffer_gdf

