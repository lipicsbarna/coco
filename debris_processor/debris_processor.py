import json
import pandas as pd
from shapely.geometry import Polygon

DEBRIS_CATEGORIES_BY_NAME = [
    "cement_block_broken",
    "brick_standard",
    "pile_of_trash",
    "electrical_wires"
]

def segmentation_to_polygon_area(segmentation: list[list]):
    segmentation = segmentation[0]
    coordinates = []
    counter = 0
    while counter < len(segmentation):
        coordinates.append([segmentation[counter], segmentation[counter + 1]])
        counter += 2
        
    return Polygon(coordinates).area

def calculate_debris_area(coco_json: dict, debris_categories: list[str]=DEBRIS_CATEGORIES_BY_NAME) -> float:
    
    categories = coco_json["categories"]
    category_dict = {
        category['id']: category["name"] for category in coco_json["categories"]
        if category["name"] in debris_categories
    }
    
    annotations: pd.DataFrame = pd.DataFrame(coco_json["annotations"])
    annotations["area"] = annotations["segmentation"].apply(lambda segmentation: segmentation_to_polygon_area(segmentation))
    debris_area = annotations[annotations["category_id"].isin(category_dict.keys())]["area"].sum()
    not_debris_area = annotations[~annotations["category_id"].isin(category_dict.keys())]["area"].sum()
    
    return debris_area, not_debris_area
