import re
from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent

class Kabum:
    def __init__(self) -> None:
        self.retailer_id = 'a86c4af6-572f-482c-8dff-50914970e427'

    def get_response(self, url):
            headers = { 
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
			"accept-encoding": "gzip, deflate, br", 
			"accept-language": "en", 
			"user-agent": str(UserAgent().chrome), 
		}
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
            print(site)
            print(e) 
        return price, store
