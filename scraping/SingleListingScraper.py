from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import attrs

import logging
import SeleniumSelectors

logger = logging.getLogger(__name__)


@attrs.define
class ListingInfo:
    id: str
    url: str
    title: str
    description: str
    price: str
    parameters: list[str]


class SingleListingScraper:
    """
    This is used to scrape single pages like this: https://www.olx.pl/d/oferta/bmw-e39-525i-gruz-zimowy-wojownik-CID5-ID183QVX.html
    """

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 3)

    save_file = "../data/scrapped_links.json"

    def scrape(self, url: str) -> ListingInfo:
        self.driver.get(url)

        self.accept_cookies()

        return self.get_listing_info(url)

    def accept_cookies(self):
        # wait for the cookie accept button to load in
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(SeleniumSelectors.COOKIE_ACCEPT)
            )
            element.click()
            logger.info("Accepted cookies")
        except:
            logger.warning("Accept cookies banner did not show up")

    def get_listing_info(self, url: str) -> ListingInfo:
        # This contains uncleaned data, but I think it will be easier to clean up after, than while scraping
        self.wait.until(
            EC.visibility_of_element_located(SeleniumSelectors.LISTING_PARAMETERS)
        )
        return ListingInfo(
            price=self.driver.find_element(*SeleniumSelectors.LISTING_PRICE).text,
            url=url,
            title=self.driver.find_element(*SeleniumSelectors.LISTING_TITLE).text,
            id=self.driver.find_element(*SeleniumSelectors.LISTING_ID).text,
            description=self.driver.find_element(*SeleniumSelectors.LISTING_DESCRIPTION).text,
            parameters=[p.text for p in self.driver.find_element(*SeleniumSelectors.LISTING_PARAMETERS).find_elements(*selenium_selectors.LISTING_PARAMETER)]
        )



