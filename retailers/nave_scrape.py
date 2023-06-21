from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from requests_html import HTMLSession


class Nave:
    def __init__(self) -> None:
        self.retailer_id = '4e872480-c21c-4e68-b2b0-9c0515d5819b'

    def get_response(self, url):
        ua = str(UserAgent().chrome)
        headers = {'User-Agent': ua}
        r = requests.get(url, headers=headers)
        return r
    
    def bestCashbackFinder(self):
        return None

    def coupon_validation(self, description, product):
        return True

    def scrape(self, url, **kwargs):
        ua = str(UserAgent().chrome)
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
        price = -1
        try:
            r = session.get(url)
            r.html.render(sleep=5)
        except Exception as e:
            print(e)
            price = -2
            session.close()
            return None, None
        try:
            price = float(BeautifulSoup(r.html.raw_html, 'html.parser').find('span', class_='lojanave-product-price-0-x-sellingPriceValue').text[3:].replace('.', '').replace(',', '.'))
        except Exception as e:
            print('Erro no produto da Nave', e)
        r.close()
        session.close()
        return price, 'Nave'

if __name__ == '__main__':
    print(Nave().scrape('https://www.navegamer.com.br/notebook-gamer-nave-estelar-gm5ag0o/p'))
    
