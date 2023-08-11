from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from requests_html import HTMLSession


class Samsung:
    def __init__(self) -> None:
        self.retailer_id = '908ee6f0-2d53-4fb3-b0aa-80970c2efb22'

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
        # fullPrice = None
        try:
            r = session.get(url)
            r.html.render(sleep=5)
        except Exception as e:
            print(e)
            price = -2
            session.close()
            return None, None
        try:
            # fullPrice = float(BeautifulSoup(r.html.raw_html, 'html.parser').find('div', class_='samsungbr-app-pdp-2-x-contentInstallmentPrice').find('span', class_='samsungbr-app-pdp-2-x-currencyContainer').text[3:].replace('.', '').replace(',', '.'))
            price = float(BeautifulSoup(r.html.raw_html, 'html.parser').find('span', class_='samsungbr-app-pdp-2-x-spotPrice').text[3:].replace('.', '').replace(',', '.'))
        except Exception as e:
            print('Erro no produto da Samsung', e)
        r.close()
        session.close()
        return price, 'Samsung'

if __name__ == '__main__':
    print(Samsung().scrape('https://shop.samsung.com/br/samsung-galaxy-book3-ultra-intel-core-i9/p'))
    
