from bs4 import BeautifulSoup
from requests_html import HTMLSession
from fake_useragent import UserAgent

class Asus:
    def __init__(self) -> None:
        self.retailer_id = '19da6aa1-5f84-48b7-bdec-536a0798a520'
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
            price = float(BeautifulSoup(r.html.raw_html, 'html.parser').find('span', class_='price').text[3:].replace('.', '').replace(',', '.'))
        except Exception as e:
            print('Erro no produto da Asus', e)
        r.close()
        session.close()
        return price, 'Asus'

if __name__ == '__main__':
    print(Asus().scrape('https://compre.vc/v2/13895e0ace5'))