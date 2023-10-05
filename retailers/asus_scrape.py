from bs4 import BeautifulSoup
from requests_html import HTMLSession
from fake_useragent import UserAgent

class Asus:
    def __init__(self) -> None:
        self.retailer_id = '19da6aa1-5f84-48b7-bdec-536a0798a520'
    def coupon_validation(self, description, product):
        return True 
    
    def bestCashbackFinder(self):
        return None

    def scrape(self, url, **kwargs):
        ua = str(UserAgent().chrome)
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
        price = -1
        try:
            r = session.get(url)
            r.html.render(sleep=8, timeout=20)
        except Exception as e:
            print(e)
            price = -2
            session.close()
            return None, None
        soup = BeautifulSoup(r.html.raw_html, 'html.parser')
        
        try:
            price_tag = soup.find('meta', {'itemprop': 'price'})['content']
            price = float(price_tag)
        except Exception as e:
            print('Erro no produto da Asus', e)
        r.close()
        session.close()
        return price, 'Asus'

if __name__ == '__main__':
    print(Asus().scrape('https://br.store.asus.com/notebook-asus-vivobook-16x-k3605zf-n1198w-preto.html?utm_term=23078451&utm_source=lomadee&utmi_cp=lomadee&utm_medium=afiliado&utm_campaign=cpa&lmdsid=NjExMSwzNzQ1NTkxNywxNjk2NTE0MjExMjk4LG51bGwsNzg5NywyMzIxZWI5ZmQwNiwlmdhjacfrlaalrfweal'))