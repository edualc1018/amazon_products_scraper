import time

from utils.products import scrape_products
from utils.settings import get_search_terms, get_delay

if __name__ == "__main__":
    for search_term in get_search_terms():
        scrape_products(search_term)
        print("Pausing for a bit...\n")
        time.sleep(get_delay()["search"])
