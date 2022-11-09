from pydantic import BaseModel
from typing import List, Optional

class Furniture(BaseModel):
    """Class for base properties of furniture"""
    furniture_name: str
    furniture_description: str
    furniture_price = str
    furniture_image_links: List[str]
    furniture_stock_in_store: int
    furniture_key_features: str
    

class FurnitureLink(BaseModel):
    url: str