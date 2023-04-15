from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

url = 'https://click.linksynergy.com/deeplink?id=HWP*/f3BEF0&mid=47364&murl=https%3A%2F%2Fwww.lenovo.com%2Fbr%2Fpt%2Flaptops%2Flaptops-legion%2Flegion-5-series%2FLegion-5i-Gen-7-15-inch-Intel%2Fp%2FLEN101G0016%3F'
class Lenovo:
    def __init__(self) -> None:
         self.retailer_id = '87417cba-be9a-49c4-91a2-ed930d7dca2f'

    def coupon_validation(self, description, product):
        return True

    def get_response(self, url):
            ua = str(UserAgent().chrome)
            headers = {'User-Agent': ua}
            r = requests.get(url, headers=headers)
            return r

    def scrape(self, url, **kwargs):
        price = -2
        site = BeautifulSoup(self.get_response(url).content, 'html.parser')
        try:
            price = float(site.find('dd', {'itemprop': 'price'}).text[3:].replace('.', '').replace(',', '.'))
            stock_msgs = site.findAll('span', {'class': 'stock_message'})
            count = 0
            for msg in stock_msgs:
                if msg.text == 'Esgotado':
                    count += 1
            if count == len(stock_msgs):
                price = -1
        except Exception as e:
            price = -2
            print(e)
        return price, 'Lenovo'

if __name__ == '__main__':
    print(Lenovo().scrape(url))