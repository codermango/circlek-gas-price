import requests
from bs4 import BeautifulSoup
import csv
import os.path
from os import path

PRICES_CSV_FILE = '../prices.csv'


class CirclekCrawler(object):
    def __init__(self, url):
        self.__prices = None
        self.__url = url

    def crawler_prices(self):
        res = requests.get(self.__url)
        soup = BeautifulSoup(res.text, "html.parser")
        price_cells = soup.find_all('td', {"headers": 'view-price-gross-table-column'})
        date_cells = soup.find_all('td', {"headers": 'view-field-price-date-table-column'})
        price_list = [float(td.span.next_sibling.strip().replace(",", ".")) for td in price_cells]
        date_list = [td.time.text.strip() for td in date_cells]

        self.__prices = [
            {"product": "95", "price": price_list[0], "date": date_list[0]},
            {"product": "98", "price": price_list[1], "date": date_list[1]},
            {"product": "98_plus", "price": price_list[2], "date": date_list[2]}
        ]

    def save_prices(self):
        if path.exists(PRICES_CSV_FILE):
            with open(PRICES_CSV_FILE, 'a', newline="") as csvfile:
                fieldnames = ['product', 'price', 'date']
                writer = csv.DictWriter(csvfile, fieldnames)
                for p in self.__prices:
                    writer.writerow(p)

        else:
            with open(PRICES_CSV_FILE, 'a', newline="") as csvfile:
                fieldnames = ['product', 'price', 'date']
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writeheader()
                for p in self.__prices:
                    writer.writerow(p)

    def daily_job(self):
        self.crawler_prices()
        self.save_prices()

    @property
    def price95(self):
        return self.__prices[0]

    @property
    def price98(self):
        return self.__prices[1]

    @property
    def price98_plus(self):
        return self.__prices[2]

    @property
    def prices(self) -> list:
        return self.__prices


# cc = CirclekCrawler("https://www.circlek.se/drivmedelspriser")
# cc.crawler_prices()
# print(cc.price95)
# cc.save_prices()
