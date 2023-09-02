from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from requests_html import HTMLSession, user_agent
import re

class MercadoLivre:
    def __init__(self) -> None:
        self.retailer_id = 'b78e8a3d-31ad-433a-9d2b-94068ef0368c'
            
    def bestCashbackFinder(self):
        return None

    def get_response(self, url):
            ua = str(UserAgent().chrome)
            headers = {'User-Agent': ua}
            r = requests.get(url, headers=headers)
            return r
    def coupon_validation(self, description, product):
        # if description:
        #     description = json.loads(description)
        #     try:
        #         if product['category']['name'] not in description['category']:
        #             return False
        #     except:
        #         pass
        return True
      
    def extract_discounts(self, text, price):
      # Extract percentage discount
      percentage_discount = re.search(r'(\d+)%\s+OFF', text)
      if percentage_discount:
          percentage_discount = float(percentage_discount.group(1))/100
          return price * percentage_discount

      # Extract fixed amount discount
      fixed_discount = re.search(r'R\$(\d+)', text)
      if fixed_discount:
          return float(fixed_discount.group(1))

      return 0

    def scrape(self, url, **kwargs):
        # response = self.get_response(url)
        # response = self.get_response(url)
        price = -2
        try:
            session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+user_agent()])
            r = session.get(url)
            r.html.render(sleep = 2)

        except Exception as e:
            session.close()
            r.close()
            print(e)
            return None, None
        soup = BeautifulSoup(r.html.raw_html, 'html.parser')
        
        productUrl = soup.find('div', {'class': 'ui-eshop-item__data ui-eshop-item__data--row'})['href']
        
        print(productUrl)
        
        try:
          r = session.get(productUrl)
          r.html.render(sleep = 2)
        except Exception as e: print(e)
        
        r.close()
        session.close()
        
        soup = BeautifulSoup(r.html.raw_html, 'html.parser')
        
        try:
            price = soup.find_all('span', {"class": "andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"})[0].find('span', {'class': 'andes-money-amount__fraction'}).text
            price = float(price.replace('.', '').replace(',', '.'))
            
            coupons_element = soup.find_all('li', {'class': 'ui-vpp-tag-limited__list-item'})
            
            pix_discount_element = soup.find('div', {'class': 'ui-pdp-price__tags'})
            pix_discount = 0
            if(pix_discount_element):
              pix_discount = self.extract_discounts(pix_discount_element.text, price)
            
            discounts_ammout = []
            for element in coupons_element:
              discounts_ammout.append(self.extract_discounts(element.text, price))
            
            max_discount = max(discounts_ammout)
            
            print('Desconto pix: ', pix_discount)
            print('Desconto cupom: ', max_discount)
            price = price - max_discount - pix_discount
            
            print('Preço final: ', price)
                                    
        except Exception as e:
            print(e)
        return price, 'Mercado Livre'

if __name__ == '__main__':
    print(MercadoLivre().scrape('https://mercadolivre.com.br/sec/281vgPF'))