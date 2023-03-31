from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from api import api
import json

class Girafa:
    def __init__(self) -> None:
        self.retailer_id = 'b28ea917-ad45-4be5-9d39-7ee97c5363ed'

    def coupon_validation(self, description, product):
        return True

    def scrape(self, url, **kwargs):
        price = -1
        store = 'Girafa'
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
            price = float(site.find_all('span', class_='desconto-produto')[0].text.strip()[3:].replace('.', '').replace(',', '.'))
        except:
            pass
        coupon = site.find('div', class_='boxCupom-produto')
        if coupon:
            code = coupon.find_all('div')[1].find_all('p')[1].find('b').text
            discount = coupon.find_all('div')[1].find_all('p')[2].find('span').text
            data = {'code': code, 'discount': discount, 'retailer_id': kwargs['retailer_id'], 'available': True, 'description': 'auto-find-coupon'}
            r = api.create_coupon(data)
        else:
            coupons = api.get_coupons(kwargs['retailer_id'])
            for coupon in coupons:
                if coupon['description'] == 'auto-find-coupon':
                    r = api.delete_coupon(coupon['id'])
        return price, store
    

if __name__ == '__main__':
    g = Girafa()
    g.scrape('https://compre.vc/v2/3235c27147')