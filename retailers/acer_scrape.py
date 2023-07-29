from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import json
from api import api
from dotenv import load_dotenv
from lxml import etree
import re
import os
from requests_html import HTMLSession

load_dotenv()

MAIN_URL, API_KEY = (os.getenv('MAIN_URL'), os.getenv('API_KEY'))
class Acer:
    def __init__(self) -> None:
        self.retailer_id = '54f99110-bc6a-4c4f-abf8-99299aba16dd'
        self.cashbackProviders = [
            {
                "name": "Cuponomia",
                "affiliatedLink": "https://www.cuponomia.com.br/ref/a8a8ec1cba89",
                "url": "https://www.cuponomia.com.br/desconto/acer",
                "xpath": "/html/body/section[1]/div[1]/div[1]/div/aside/a/span",
                "xpath2": "/html/body/section[2]/div[1]/div[1]/div/aside/a/span",
            },
            {
                "name": "Meliuz",
                "affiliatedLink": "https://www.meliuz.com.br/i/ref_bae7d6a1?ref_source=2",
                "url": "https://www.meliuz.com.br/desconto/cupom-acer",
                "xpath": "/html/body/div[3]/div[4]/button",
                "xpath2": "/html/body/div[3]/div[4]/button",
            }
        ]
    
    def bestCashbackFinder(self):
        cashback = {}
        try:
            for cashbackProvider in self.cashbackProviders:
                r = self.get_response(cashbackProvider["url"])
                soup = BeautifulSoup(r.content, "html.parser")   

                dom = etree.HTML(str(soup))
                
                try: cashbackFullLabelArray = dom.xpath(cashbackProvider["xpath"])[0].text.split(" ")
                except:
                    try: cashbackFullLabelArray = dom.xpath(cashbackProvider["xpath2"])[0].text.split(" ")
                    except: pass

                
                ## gambiarra
                cashback_from_coupon = api.get_coupon('a4e0d2ba-b3ae-41f0-ba3f-fe63a9aefe94')
                if cashbackProvider['name'] == 'Meliuz':
                    cashbackFullLabelArray = [cashback_from_coupon['discount']]
                ## 
        
                for label in cashbackFullLabelArray:
                    if "%" in label:
                        cashbackProvider["value"] = float(
                            label[: label.find("%")].replace(",", ".")
                        )
                        if not cashback or cashback["value"] < cashbackProvider["value"]:
                            cashback = cashbackProvider
                print(cashback)
        except Exception as e:
            print("erro na busca de cashbacks", e)
            cashback = None
        
        return cashback
    
    def get_response(self, url):
        ua = str(UserAgent().chrome)
        headers = {'User-Agent': ua}
        r = requests.get(url, headers=headers)
        return r
    
    def coupon_validation(self, description, product):
        if description:
            try:
                #description = json.loads(description)
                if description == 'CASHBACKNOTALLOWED': return True 
                if product['id'] not in description:
                    return False
            except Exception as e:
                pass
        return True
    
    def cashback_validation(self, couponDescription, product):
        if couponDescription:
            try:
                if product['cashback']['name'] in couponDescription:
                    return False
            except Exception as e:
                pass
        return True
            
    def scrape(self, url, **kwargs):
        
        productId = kwargs['product_id']
        print(productId)
        response = self.get_response(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        available_status = soup.find('span', class_='b vtex-rich-text-0-x-strong') or soup.find('div', class_='vtex-availability-notify-0-x-title t-body mb3')
        if available_status:
            return -1, None
        coupons = soup.find_all('div', class_='vtex-flex-layout-0-x-flexColChild vtex-flex-layout-0-x-flexColChild--flagCoupon pb0')
        server_coupons =  api.get_coupons(self.retailer_id)
        cupom_value = 0
        i = 0
        try:
            for cupom in coupons:
                i += 1
                if cupom.text:
                    cupom_value = i*100
                    #print('Cupom de {} reais'.format(cupom_value) + ': ' + str(cupom_value) + 'off')
                    data = {'code': str(cupom_value) + 'off', 'discount': str(cupom_value), 'retailer_id': kwargs['retailer_id'], 'available': True, 'description': kwargs['product_id']}
                    
                    flag = 0
                    for serverCoupon in server_coupons:
                        if serverCoupon['code'].upper() == data['code'].upper():
                            print(serverCoupon['code'], data['code'])
                            
                            coupon_description = serverCoupon['description']
                            if kwargs['product_id'] not in coupon_description:
                                newCouponDescription = coupon_description +" "+ kwargs['product_id']
                                newCouponDescriptionStr = json.dumps(newCouponDescription)
                                r = api.update_coupon(serverCoupon['id'], {"description": newCouponDescriptionStr})
                            flag = 1
                    if flag == 0:
                        r = api.create_coupon(data)
                        print(r.content)
        except Exception as e:
            raise
        if cupom_value == 0:
            for coupon in server_coupons:
                try:
                    if json.loads(coupon['description'])['product_id'] == kwargs['product_id']:
                        api.delete_coupon(coupon['id'])
                except:
                    pass
        
            
        #print(soup)
        try:
            preco = soup.find('span', class_= 'vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--productPage-sellingPrice vtex-product-price-1-x-currencyContainer--productPage-sellingPrice-stickyInfoProducts').text
            #preco = precos[0].text
            preco_value = float(preco[3:].replace('.', '').replace(',', '.'))
            #preco_com_cupom = preco_value - cupom_value ## Na versão final, fazer a comparação entre cupons a partir do banco de dados
            preco_final_pix = preco_value*0.88
        except Exception as e:
            print('Não foi possível encontrar o preço na página.')
            return None, None

        print(preco_final_pix)
        return preco_final_pix, 'Acer'

if __name__ == '__main__':
    acer = Acer()
    acer.scrape('https://adsplay.g2afse.com/click?pid=10&offer_id=1&path=https://br-store.acer.com/notebook-acer-an517-54-56q0-ci511400h-8gb-1tb-256gb-ssd-4g-gddr6-wnhcsl64-black-17-3-fhd-nh-qegal-001/p', retailer_id = '54f99110-bc6a-4c4f-abf8-99299aba16dd', product_id = 'e3708b15-c0cb-41d0-9240-e0937f125d96')