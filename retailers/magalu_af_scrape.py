from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import json

class MagaluParceiro:
    def __init__(self) -> None:
        self.retailer_id = 'f4eaafb2-1e11-49b4-89e8-cc68c848ea84'
            
    def bestCashbackFinder(self):
        return None

    def get_response(self, url):
            ua = str(UserAgent().chrome)
            headers = {'User-Agent': ua}
            r = requests.get(url, headers=headers)
            return r
    def coupon_validation(self, description, product):
        if description:
            try:
                if description == 'CASHBACKNOTALLOWED': return True 
                if product['id'] not in description:
                    return False
            except:
                pass
        return True

    def scrape(self, url, **kwargs):
        response = self.get_response(url)
        price = -2
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            price = soup.find('p', {"data-testid": "price-value"}).text[2:]
            price = float(price.replace('.', '').replace(',', '.'))
        except Exception as e:
            print(e)
        return price, 'Magalu'

if __name__ == '__main__':
    print(MagaluParceiro().scrape('https://www.magazinevoce.com.br/magazineotcm/monitor-gamer-lg-24-hdmidisplayport-led-full-hd-144hz-1ms-mbr-freesync-ajuste-de-inclinacao/p/edfj76cbh5/IN/MNPC/'))