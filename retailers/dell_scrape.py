import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Dell:
    def __init__(self) -> None:
        self.retailer_id = 'b43b67ad-a6f4-4525-8a8e-31a829e81c39'

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
            price = float(site.find('span', {'class': 'h3 font-weight-bold mb-1 text-nowrap sale-price'}).text[3:].replace('.', '').replace(',', '.'))
        except Exception as e:
            print(e)
            
        return price, 'Dell'

if __name__ == '__main__':
    print(Dell().scrape('https://www.dell.com/pt-br/shop/cty/notebook-gamer-dell-g15/spd/g-series-15-5520-laptop'))
