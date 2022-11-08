from scraping.scrapers.base import BaseScraper
from scraping.models.furniture import Furniture, FurnitureLink
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup


class Ikea(BaseScraper):
    __items_per_page__: int = 20
    __domain__: str = "https://www.15min.lt/"

    def _retrieve_items_list(self, results_count: int, keyword: str) -> List[FurnitureLink]:
        """Method to search recipes by keyword and save specifed number of results."""
        results: List[FurnitureLink] = []
                
        for page_num in enumerate(results_count):
            content = self._get_page_content(f"maistas/receptai/paieska?f%5Bphrase%5D={keyword}&s={page_num}")
            if content:
                recipes_list_div = content.find("div", class_ = "recipe-list")
                if not recipes_list_div:
                    break  
            # aprasome html koses elementa is kurios surinksim info
            all_recipe_divs = recipes_list_div.find_all("div", class_="list-row")        
            for recipe_div in all_recipe_divs:                
                recipe_link = recipe_div.find("a").get("href")
                results.append(FurnitureLink(url = recipe_link))

        return results

    def _extract_ingredients(self, content: BeautifulSoup) -> str:
        """Method to get ingredients of the recipe."""
        all_ingredients: List[Dict] = []
        
        recipe_ingredients = content.find("ul", class_="ingredients").find_all("li")
        for ingredient in recipe_ingredients:
            ingredient_span = ingredient.find_all("span")
            all_ingredients.append({
                "ingredient_name": ingredient_span[0].text.strip(),
                "ingredient_amount": ingredient_span[2].text.strip(),
                "ingredient_note": ingredient_span[3].text.strip()
            })
        return str(all_ingredients)
    
    def _extract_making_steps(self, content: BeautifulSoup) -> str:
        """Method to get recipe's making steps."""
        recipe_manual: List[str] = []
        recipe_making_steps = content.find("div", class_="description text").find_all("p")

        for step in recipe_making_steps:
            step_to_txt = step.text.strip()
            recipe_manual.append(step_to_txt)    
        return "\n".join(recipe_manual)

    def _retrieve_recipe_info(self, link: FurnitureLink) -> Optional[Furniture]:
        """Method to get main info about recipe."""
        content = self._get_page_content(link.url)

        if content:
            try:
                recipe_title = content.find("h3").text.strip().split('\n')[0]
                recipe_amount = content.find("span").text
            except AttributeError:
                return None

            try:
                main_recipe_image = content.find("div", class_ = "badge-layers-holder").find("img").get("src")
            except KeyError:
                main_recipe_image = None

            return Furniture(
                recipe_title = recipe_title,
                recipe_image_link = main_recipe_image,
                recipe_amount = recipe_amount,
                ingredients = self._extract_ingredients(content),
                making_steps = self._extract_making_steps(content),
            )
        else:
            return None
