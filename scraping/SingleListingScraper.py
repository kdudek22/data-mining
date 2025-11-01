import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import attrs

import logging
from scraping import SeleniumSelectors

logger = logging.getLogger(__name__)


@attrs.define
class ListingInfo:
    id: str
    url: str
    title: str
    description: str
    price: str
    parameters: list[str]
    views: str


class SingleListingScraper:
    """
    This is used to scrape single pages like this: https://www.olx.pl/d/oferta/bmw-e39-525i-gruz-zimowy-wojownik-CID5-ID183QVX.html
    """

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 3)
    accepted_cookies: bool = False  # as you should only have to accept them once, and it saves us a lot of time

    def scrape(self, url: str) -> ListingInfo | None:
        time.sleep(random.randint(0, 10))  # they time out if we do it too fast :)
        self.driver.get(url)

        if not self.accepted_cookies:
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
            self.accepted_cookies = True
        except:
            logger.warning("Accept cookies banner did not show up")

    def get_listing_info(self, url: str) -> ListingInfo:
        try:
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
                parameters=[p.text for p in self.driver.find_element(*SeleniumSelectors.LISTING_PARAMETERS).find_elements(*SeleniumSelectors.LISTING_PARAMETER)],
                views=self.driver.find_element(*SeleniumSelectors.LISTING_VIEWS).text,
            )
        except:
            logger.error(f"Could not get listing info for {url}")


