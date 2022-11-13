from scraping.models.furniture import Furniture, FurnitureLink
from typing import List, Optional
from abc import ABC, abstractmethod
import math
from bs4 import BeautifulSoup
import requests

# abstrakti klase - ja inicializuoti nera logiska, tik paveldeti
class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""
      
    @abstractmethod
    def _retrieve_item_links(self, results_count: int, keyword: str) -> List[FurnitureLink]:
        """Method to get items links searching by keyword and save specifed number of results."""
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        """Method to get needed content from search result page or whatever related page."""
        resp = requests.get(query)
        if resp.status_code == 200:
            return BeautifulSoup(resp.content)
        raise Exception("Cannot get content. Site is unreachable.")

    def _retrieve_furniture_info(self, link: FurnitureLink) -> Optional[Furniture]:
        pass

    def scrape(self, results_count: int, keyword: str) -> List[Furniture]:
        try:
            pages_count = math.ceil(results_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise Exception("Forgot to set how many items is displayed per page.")
        furniture_links = self._retrieve_item_links(results_count, keyword)
        scraped_recipes: List[Furniture] = []
        for recipe_link in furniture_links:
            scraped_recipe = self._retrieve_furniture_info(recipe_link)
            if scraped_recipe is not None:
                scraped_recipes.append(scraped_recipe)
        return scraped_recipes