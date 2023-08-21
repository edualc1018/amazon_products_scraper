import requests
import csv
import time

from bs4 import BeautifulSoup, Tag
from utils import file
from fake_useragent import UserAgent

from typing import List, Dict

from . import settings

search_url = "https://www.amazon.com/s?k={}&page={}&ref=nb_sb_noss_2"
ua = UserAgent()


def get_headers() -> Dict:
    return {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "cache-control": "max-age=0",
        "cookie": settings.get_cookie_string(),
        "user-agent": ua.random,
    }


def check_item(item, html: [Tag], is_one: bool, class_name=None, id=None):
    if not item:
        if class_name is not None:
            if is_one:
                return html.find(class_=class_name)
            return html.find_all(class_=class_name)
        return html.find(id=id)
    # if it is not empty just return it
    return item


def process_data(scrape_products, search_term) -> None:
    file.create_dir("data")
    file_name = search_term.lower().replace(" ", "_")
    base_dir = file.get_base_directory()
    file_path = file.check_filename(f"{base_dir}/data/{file_name}.csv")
    if settings.get_group() is not False:
        file_path = file.insert_before(file_path, settings.get_group())
        file.create_dir("data", settings.get_group())
    title = {
        "name": "Product Name",
        "price": "Price",
        "ratings": "Ratings",
        "image": "Product Image",
        "link": "Product Link",
    }
    write_csv(title, file_path)
    for product in scrape_products:
        # Initial search for product_name
        product_name = product.find(
            "span", {"class": "a-size-medium a-color-base a-text-normal"}
        )
        # Version 2 search if the initial search produces no results
        product_name = check_item(
            product_name,
            product,
            True,
            "a-size-base-plus a-color-base a-text-normal",
        )
        # Initial search for product_price
        product_price = product.find("span", {"class": "a-offscreen"})
        # Initial search for product_link
        product_link = product.find(
            "a",
            {
                "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
            },
        )
        product_rating = product.find(
            "span", {"class": "a-size-base puis-normal-weight-text"}
        )
        product_image = product.find("img", {"class": "s-image"})
        data = {
            "name": product_name.text if product_name else "No name",
            "price": product_price.text if product_price else "No price",
            "ratings": product_rating.text if product_rating else "No ratings",
            "image": product_image["src"] if product_image else "No image",
            "link": "https://www.amazon.com" + product_link["href"]
            if product_link
            else "No link",
        }
        if data["name"] != "No name":
            write_csv(data, file_path)
    print(f'Scraped data written to "{file_path}"')


def write_csv(data, file_path) -> None:
    with open(file_path, "a") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                data["name"],
                data["price"],
                data["ratings"],
                data["image"],
                data["link"],
            )
        )


def get_products(search_term, page_num, initial=False):
    url = search_url.format(search_term, page_num)
    print(f"Scraping {url}...")
    response = requests.get(url, headers=get_headers())
    soup = BeautifulSoup(response.text, "lxml")
    if settings.is_show_html():
        file.create_dir("response")
        file_name = file.path_join(
            file.get_base_directory(),
            "response",
            f"{search_term.lower().replace(' ', '_')}_page_{page_num}.html",
        )
        with open(file_name, "w") as file_writer:
            file_writer.write(soup.prettify())
        print(f'Response html is written to "{file_name}"')
    # Initial search
    products = soup.find_all(
        "div",
        {
            "class": "s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t1 puis-include-content-margin puis puis-v3b48cl1js792724v4d69zlbwph s-latency-cf-section s-card-border"
        },
    )
    # Try to find products with another class name
    class_name = "s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t1 puis-expand-height puis-include-content-margin puis puis-v3b48cl1js792724v4d69zlbwph s-latency-cf-section s-card-border"
    products = check_item(products, soup, False, "s-result-item", class_name)
    # Trying to find products using id
    id_name = "gridItemRoot"
    products = check_item(products, soup, False, id=id_name)
    if initial:
        try:
            get_max_pages = soup.select("span.s-pagination-item:nth-child(7)")[
                0
            ].text
        except IndexError:
            get_max_pages = 1
        return {
            "products": products,
            "max_pages": get_max_pages,
        }
    time.sleep(settings.get_delay()["pages"])
    return products


def scrape_products(search_term) -> None:
    # Initial scraping of the first page
    print(f"Scraping {search_term}...")
    result = get_products(search_term, 1, initial=True)
    products = result["products"]
    max_pages = (
        int(result["max_pages"])
        if settings.get_limit() == "all"
        else settings.get_limit()
    )
    if settings.get_limit() != 1:
        for counter in range(2, max_pages + 1):
            products.extend(get_products(search_term, counter))
    if products is not []:
        process_data(products, search_term)
    else:
        print("Please update the cookie string in settings.json")
