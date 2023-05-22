from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent

class Fastshop:
    def __init__(self) -> None:
         self.retailer_id = '601079a1-a602-4768-b395-9df49525c52d'
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
        return price, store
    
if __name__ == '__main__':
    c = Fastshop()
    c.scrape('https://tidd.ly/3BgvCJK', sku='3002057553_PRD')