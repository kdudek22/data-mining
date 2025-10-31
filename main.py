from scraping.ListingsScraper import ListingsScraper
from scraping.SingleListingScraper import SingleListingScraper, ListingInfo
import json
import attrs


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


def scrape_listings() -> None:
    links = [
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e39/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e36/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e30/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e34/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-e32/",
        "https://www.olx.pl/motoryzacja/samochody/q-bmw-drift/",
    ]
    res = set()
    scraper = ListingsScraper()

    for link in links:
        res = res.union(scraper.scrape(link))

    res_list = list(res)

    with open("data/results.json", "w") as json_file:
        json.dump(list(res_list), json_file, indent=4)
    logger.info(f"saved to a file {len(res_list)} links")


def scrape_single_listings() -> list[ListingInfo]:
    urls = json.loads(open("./data/listing_links.json").read())

    urls = [u for u in urls if "otomoto" not in u]  # simply filter otomoto links for now

    res = []
    scraper = SingleListingScraper()

    for (i, url) in enumerate(urls):
        try:
            listing_info = scraper.scrape(url)
            if listing_info:
                res.append(listing_info)
        except Exception as e:
            logger.exception(f"Error: {e}")

        logger.info(f"Done {i}/{len(urls)}")

    res_dict = [attrs.asdict(listing) for listing in res]

    with open("results.json", "w", encoding="utf-8") as json_file:
        json.dump(list(res_dict), json_file, indent=4, ensure_ascii=False)

    logger.info(f"saved to a file {len(res_dict)} scraped listings")


if __name__ == "__main__":
    import time
    start = time.time()
    scrape_single_listings()

    logger.info(f"Finished in {time.time() - start} seconds")

