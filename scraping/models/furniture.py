from pydantic import BaseModel
from typing import List, Optional

class Furniture(BaseModel):
    """Class for base properties of furniture"""
    furniture_name: str
    furniture_description: str
    furniture_price = int
    furniture_image_link: List[str]    
    furniture_key_features: str
    furniture_size: str
    
    #furniture_stock_in_store: int    
class FurnitureLink(BaseModel):
    url: str