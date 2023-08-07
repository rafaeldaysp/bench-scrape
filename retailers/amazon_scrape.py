from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Amazon:
    def __init__(self) -> None:
        self.retailer_id = '04901ac7-2af9-42ad-8fb6-b3fe4e9bfea6'
    def coupon_validation(self, description, product):
        return True
    
    def bestCashbackFinder(self):
        return None

    def scrape(self, url, **kwargs):
        price = -1
        store = 'Amazon'
        ua = str(UserAgent().chrome)
        try:
            session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
            r = session.get(url)
            r.html.render(sleep = 2)
        except Exception as e:
            session.close()
            r.close()
            print(e)
            return None, None
        site = BeautifulSoup(r.html.raw_html, 'html.parser')
        r.close()
        session.close()
        try:
            price = float(site.find('span', class_='a-offscreen').text[2:].replace('.', '').replace(',', '.'))
        except:
            try:
                label = site.find('span', class_='a-color-price a-text-bold').text
                if 'Não disponível' in label: return -1, 'Amazon'
            except:
                price = -2
        return price, store


if __name__ == '__main__':
    amazon = Amazon()
    print(amazon.scrape('https://amzn.to/420tlh5'))