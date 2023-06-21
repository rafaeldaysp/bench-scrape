from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Girafa:
    def __init__(self) -> None:
        self.retailer_id = '1c970725-5764-48ba-b012-4f2e5ed3db7a'

    def coupon_validation(self, description, product):
        return True
    
    def bestCashbackFinder(self):
        return None

    def scrape(self, url, **kwargs):
        price = -1
        store = 'Terabyte'
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+str(UserAgent().chrome)])
        try:
            r = session.get(url)
        except:
            return None, None
        r.html.render(sleep=3)
        site = BeautifulSoup(r.html.raw_html, 'html.parser')
        r.close()
        session.close()
        try:
            price = float(site.find('p', class_='val-prod valVista').text.strip()[3:].replace('.', '').replace(',', '.'))
        except Exception as e:
            print(e)
        
        return price, store
    

if __name__ == '__main__':
    g = Girafa()
    print(g.scrape('https://www.terabyteshop.com.br/produto/20337/ssd-wd-green-sn350-1tb-m2-nvme-leitura-3200mbs-e-gravacao-2500mbs-wds100t3g0c'))