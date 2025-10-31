from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from scraping import SeleniumSelectors

import logging

logger = logging.getLogger(__name__)


class ListingsScraper:
    """
    This is used to scrape links from olx search pages like: https://www.olx.pl/motoryzacja/samochody/q-bmw-e39/
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    save_file = "../data/scrapped_links.json"

    def scrape(self, link: str) -> set[str]:
        self.driver.get(link)
        logger.info("Opened page")

        self.accept_cookies()
        scrapped_links = self.scrape_listings()

        return scrapped_links

    def scrape_listings(self) -> set[str]:
        listings_links = set()

        while True:
            self.wait.until(EC.visibility_of_element_located(SeleniumSelectors.LISTINGS))  # wait for listings to load
            listings = self.driver.find_elements(*SeleniumSelectors.LISTINGS)

            for listing in listings:
                listing_link = listing.find_element(*SeleniumSelectors.LISTING_LINK).get_attribute("href")
                logger.info(f"Listing link: {listing_link}")

                listings_links.add(listing_link)  # as the promoted offers are repeated we use a set

            has_next_page = self.check_if_element_exists(SeleniumSelectors.LISTINGS_NEXT_PAGE)

            if not has_next_page:  # if there is not another page, exit the loop
                logger.info("No more pages found")
                break

            # craft the next page link and open it
            next_page_url = self.get_next_page_url(self.driver.current_url)
            self.driver.get(next_page_url)

        return listings_links

    def accept_cookies(self):
        try:
            # wait for the cookie accept button to load in
            element = self.wait.until(
                EC.visibility_of_element_located(SeleniumSelectors.COOKIE_ACCEPT)
            )
            element.click()
            logger.info("Accepted cookies")
        except:
            logger.info("Accept cookies banner did not show up")

    def check_if_element_exists(self, selector) -> bool:
        return bool(self.driver.find_elements(*selector))

    @staticmethod
    def get_next_page_url(page_url: str) -> str:
        # this is done because pressing the next page link turned out to be a bit problematic
        # I could not figure out a way to wait for the new items to get loaded in, so instaed of that
        # we simply construct a new url and load it
        parsed_url = urlparse(page_url)
        query_params = parse_qs(parsed_url.query)

        # if no page query parameter, the value should be 1, else increment the value of the page
        query_params["page"] = [str(int(query_params.get("page", [1])[0]) + 1)]

        # return the newly created link
        return urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
