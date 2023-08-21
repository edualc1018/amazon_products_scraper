# Amazon Product Scraper

A simple scraper for amazon products and saves into csv file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

Installing with virtualenv (Optional)
```sh
$ python3 -m virtualenv .venv
# pip install virtualenv
$ source .venv/bin/activate # For linux
$ .\Scripts\Activate.ps1 # For windows
```

Then clone the repository and install the required packages

```sh
$ git clone https://github.com/edualc1018/amazon_products_scraper.git
$ cd amazon_products_scraper
$ pip install -r requirements.txt
```


## Usage

This scraper can be start using:

```sh
$ python app.py
```

## Configuration

The `settings.json` file provide some configuration on the scraper

*search_term*
- List of searches you want to scrape.

*group*
- Default to false. When set to any string for example "search_group_1" will save all the csv file in the folder with the name "search_group_1" inside the folder data.

*cookie_string*
- This is needed for the scraper to work.
- I'll provide a tuturial how to get this.

*pages*
- Set the number of pages to scrape in the search result provided that the number of set pages is not greater than the maximum pages found in the search results.

*delay*
- Sets a delay while scraping. Let's not overload the website with requests.
- the `pages` option sets the delay of scraping between pages for each search term.
- the `search` option sets the delay for each search term.

*show_html*
- Saves the html response for each scraped pages.


## Features

- Explore by yourselves.

## Contributing

If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.


## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For inquiries or feedback, contact [edualc1018@gmail.com](mailto:edualc1018@gmail.com).