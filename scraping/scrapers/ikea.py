from scraping.scrapers.base import BaseScraper
from scraping.models.furniture import Furniture, FurnitureLink
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup


class Ikea(BaseScraper):
    __items_per_page__: int = 40
    __domain__: str = "https://www.ikea.lt"

    def _retrieve_items_links(self, results_count: int, keyword: str) -> List[FurnitureLink]:
        """Method to search furnitures by keyword and save specifed number of results."""
        results: List[FurnitureLink] = []        
        pages_to_iterate: int = (results_count // self.__items_per_page__) + 1 # kiek paieskos rezultatu puslapiu naudoti        
        
        for page_num in range(1, pages_to_iterate + 1):
            content = self._get_page_content(f"/lt/search/?q={keyword}&page={page_num}")
            max_number_of_pages = int(content.find("ul", class_="pagination mb-0").find_all("li", class_="page-item")[3].text)
            
            if content:
                if max_number_of_pages >= pages_to_iterate:                        
                    all_items_per_page = content.find_all("div", class_="col-6 col-md-4 col-lg-3 p-0 itemBlock")
                    counter = 1
                                                                        
                    for item in all_items_per_page:
                        link = item.find("div", class_="itemInfo").a.get("href")
                        item = f"{self.__domain__}{link}"                  
                                        
                        while results_count >= counter:          
                            results.append(FurnitureLink(url = item))
                            counter += 1
                else: 
                    print(f"Search does not contain {results_count} results.")
                    break
            if not content:
                break

        return results



    # _extract_ingredients
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




    #_retrieve_recipe_info
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
                furniture_name = recipe_title,
                furniture_description = main_recipe_image,
                furniture_price = recipe_amount,
                furniture_image_link = List[str],
                furniture_stock_in_store = int,
                furniture_key_features = str,
                furniture_care_instructions = str,

                ingredients = self._extract_ingredients(content),
                making_steps = self._extract_making_steps(content)
            )
        else:
            return None
