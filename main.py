from scraping.ListingsScraper import ListingsScraper
import json


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


def scrape_listings(url: str) -> set[str]:
    scraper = ListingsScraper()

    return scraper.scrape(url)


if __name__ == "__main__":
    links = [
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e39/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e36/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e30/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e34/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e32/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-drift/",
    ]
    res = set()

    for link in links:
        res = res.union(scrape_listings(link))

    res_list = list(res)

    with open("results.json", "w") as json_file:
        json.dump(list(res_list), json_file, indent=4)
    logger.info(f"saved to a file {len(res_list)} links")


