import re
from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent

class Kabum:
    def __init__(self) -> None:
        self.retailer_id = '8ec7eb4c-22bb-48fa-a819-7690838430d7'

    def get_response(self, url):
            ua = str(UserAgent().chrome)
            headers = {'User-Agent': ua, 'Accept-Language': 'pt-br,en;q=0.8', 'Accept-Encoding': 'br, gzip, deflate', 'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            r = requests.get(url, headers=headers)
            return r

    def coupon_validation(self, description, product):
        if description:
            description = json.loads(description)
            try:
                if product['category']['name'] not in description['category']:
                    return False
            except:
                pass
            try:
                if product['id'] not in description['product_id']:
                    return False
            except:
                pass
        return True

    def scrape(self, url, **kwargs):
        price = -1
        store = None
        response = self.get_response(url)
        try:
            site = BeautifulSoup(response.content, 'html.parser')
            price = float(site.find('h4', class_=re.compile('finalPrice')).text[3:].replace('.', '').replace(',', '.'))
            store = site.find('div', class_=re.compile('generalInfo')).find('b').text
        except Exception as e:
            print(e) 
        return price, store
