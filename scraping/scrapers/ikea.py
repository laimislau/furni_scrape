from scraping.scrapers.base import BaseScraper
from scraping.models.furniture import Furniture, FurnitureLink
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup


class Ikea(BaseScraper):
    __items_per_page__: int = 10
    __domain__: str = "https://www.ikea.lt"

    def _retrieve_item_links(self, results_count: int, keyword: str) -> List[FurnitureLink]:
        """Method to search furnitures by keyword and save specifed number of results."""
        results: List[FurnitureLink] = []        
        pages_to_iterate = (results_count // self.__items_per_page__) + 1 # kiek paieskos rezultatu puslapiu naudoti        
        
        for page_num in range(1, pages_to_iterate + 1):
            content = self._get_page_content(f"{self.__domain__}/lt/search/?q={keyword}&page={page_num}")
            pages_count = content.find("ul", class_="pagination mb-0")
            no_results = content.find("div", class_="col mt-4")
            
            if pages_count != None:
                max_number_of_pages = int(content.find("ul", class_="pagination mb-0").find_all("li", class_="page-item")[3].text)
            elif no_results != None:           
                max_number_of_pages = 0
            else:
                max_number_of_pages = 1

            if content:
                if max_number_of_pages >= pages_to_iterate:                        
                    all_items_per_page = content.find_all("div", class_="col-6 col-md-4 col-lg-3 p-0 itemBlock")
                    counter = 1

                    while results_count >= counter:                                                 
                        for item in all_items_per_page:
                            link = item.find("div", class_="itemInfo").a.get("href")
                            item = f"{self.__domain__}{link}"                                 
                            results.append(FurnitureLink(url = item))
                            counter += 1
                else: 
                    print(f"Search has less results than requested.")
                    break
            if not content:
                break

        return results


    def _extract_key_features(self, content: BeautifulSoup) -> str:
        """Method to key features of furiniture.""" 
        results: List[str] = []   
        features = content.find("div", class_="tab-pane_box").find_all("p")
        
        for feature in features: 
            feature_line = feature.text.strip()
            results.append(feature_line)       
            
        return str(results)
    
    def _extract_furniture_size(self, content: BeautifulSoup) -> str: 
        results: List[str] = []
        measures = content.find_all("div", class_="tab-pane_box")[1].find_all("tr")
        
        for measure in measures:
            measure_line = measure.text.strip()
            results.append(measure_line)
        return str(results)


    def _retrieve_furniture_info(self, link: FurnitureLink) -> Optional[Furniture]: 
        """Method to get main info about furniture."""
        content = self._get_page_content(link.url)

        if content:
            try:
                furniture_name = content.find("div", class_="d-flex align-items-center flex-wrap").h3.text
                furniture_description = content.find("h4", class_="itemFacts font-weight-normal").span.text
                furniture_price = content.find("div", class_="itemPrice-wrapper").p.span.text.replace(" €", "")
            except AttributeError:
                return None

            try:
                furniture_image_link = content.find("a", class_ = "slideImg").find("img").get("src")
            except KeyError:
                furniture_image_link = None

            return Furniture(
                furniture_name = furniture_name,
                furniture_description = furniture_description,
                furniture_price = furniture_price,
                furniture_image_link = furniture_image_link,
                furniture_key_features = self._extract_key_features(content), 
                furniture_size = self._extract_furniture_size(content), 

                #furniture_stock_in_store = int,                
            )
        else:
            return None
