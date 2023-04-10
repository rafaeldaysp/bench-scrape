from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent

class Fastshop:
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
        
        sku = kwargs['sku']
        url = f'https://apigw.fastshop.com.br/price/v0/management/price-promotion/price?store=fastshop&channel=webapp&skus={sku}&partner=parceiro-comparador&campaign=LINHA_S'
        price, store = [-1, None]
        r =  json.loads(self.get_response(url).content)
        try:
            price = r['result'][0]['products'][0]['skus'][0]['price']['payments'][0]['value']
        except:
            pass
        print(price)
        return price, store
    
if __name__ == '__main__':
    c = Fastshop()
    c.scrape('https://www.fastshop.com.br/web/p/d/SGSMG990PTO_PRD/smartphone-samsung-galaxy-s21-fe-5g-preto-128gb-6gb-ram-e-camera-tripla-de-12mp12mp8mp', sku='SGSMG990ELVRD_PRD')