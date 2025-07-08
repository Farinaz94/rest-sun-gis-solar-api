from typing import List

def generate_rasterization_chain(vector_name: str, raster_name: str, attribute_column: str):
    """
    Create a process chain to rasterize a vector layer using v.to.rast
    """
    
    return {
        "version": "1",
        "list": [
            {
                "id": "rasterize_vector",
                "module": "v.to.rast",
                "inputs": [
                    {"param": "input", "value": vector_name},
                    {"param": "output", "value": raster_name},
                    {"param": "use", "value": "attr"},
                    {"param": "attribute_column", "value": attribute_column},
                    {"param": "type", "value": "area"}
                ]
            }
        ]
    }

def generate_rseries_chain(raster_inputs: List[str], output_dsm: str):
    """
    Create a process chain to sum multiple rasters using r.series
    """
    return {
        "version": "1",
        "list": [
            {
                "id": "aggregate_dsm",
                "module": "r.series",
                "inputs": [
                    {"param": "input", "value": ",".join(raster_inputs)},
                    {"param": "output", "value": output_dsm},
                    {"param": "method", "value": "sum"}
                ]
            }
        ]
    }
