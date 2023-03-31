from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent

class Carrefour:
    def __init__(self) -> None:
         self.retailer_id = '5839a173-aff7-49a5-8ce4-cf51e4c54996'
    def coupon_validation(self, description, product):
        return True

    def get_response(self, url):
            ua = str(UserAgent().chrome)
            headers = {'User-Agent': ua}
            r = requests.get(url, headers=headers)
            return r
    def scrape(self, url, **kwargs):
        price, store = [-1, None]
        r = self.get_response(url)
        script = BeautifulSoup(r.content, 'html.parser').find('script', {'type': 'application/ld+json'})
        #print(r.content)
        try:
            data = json.loads(script.contents[0])
            price = float(data['offers']['offers'][0]['price'])
            store = data['offers']['offers'][0]['seller']['name']
        except Exception as e:
            print(r.content)
            print(e)
        return price, store
    
if __name__ == '__main__':
    c = Carrefour()
    c.scrape()