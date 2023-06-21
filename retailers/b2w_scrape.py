from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

def coupon_validation(description, product):
    return True
    
def bestCashbackFinder(self):
    return None

def scrape(url, params=None):
    price, store = [-1, None]
    ua = str(UserAgent().chrome)
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
    r = session.get(url)
    r.html.render(sleep = 3)
    site = BeautifulSoup(r.html.raw_html, 'html.parser')
    try:
        price = float(site.find('div', class_=re.compile('priceSales')).text[3:].replace('.', '').replace(',', '.'))
        try:
            store = site.find('div', class_=re.compile('offers-box')).find('p').find('a').text
        except:
            store = site.find('div', class_=re.compile('offers-box')).find('p').find('strong').text
        #tore = site.find('div', class_=re.compile('generalInfo')).find('b').text
    except Exception as e:
        pass
    r.close()
    session.close()
    print(price, store)
    return price, store

if __name__ == '__main__':
    scrape('https://www.americanas.com.br/produto/6449448606?chave=dk_hm_mo_4_2_ge&offerId=636c0298b1efc389fc3020a0')