from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


class Nave:
    def __init__(self) -> None:
        self.retailer_id = '8dabd038-474b-417e-984c-207ee9d1bf98'

    def get_response(self, url):
        ua = str(UserAgent().chrome)
        headers = {'User-Agent': ua}
        r = requests.get(url, headers=headers)
        return r

    def coupon_validation(self, description, product):
        return True

    def scrape(self, url, **kwargs):
        response = self.get_response(url)
        site = BeautifulSoup(response.content, 'html.parser')
        price = -1
        try:
            price = float(site.find('span', class_='vtex-product-price-1-x-sellingPriceValue').text[3:].replace('.', '').replace(',', '.'))
            price = price*0.95
        except Exception as e:
            print(e)
            
        return price, 'Nave'

if __name__ == '__main__':
    print(Nave().scrape('https://www.navegamer.com.br/notebook-gamer-nave-estelar-gm5ag0o/p'))