from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from requests_html import HTMLSession
from lxml import etree
from api import api

class Samsung:
    def __init__(self) -> None:
        self.retailer_id = '908ee6f0-2d53-4fb3-b0aa-80970c2efb22'
        self.cashbackProviders = [
            {
                "name": "Cuponomia",
                "affiliatedLink": "https://www.cuponomia.com.br/ref/a8a8ec1cba89",
                "url": "https://www.cuponomia.com.br/desconto/samsung",
                "xpath": "/html/body/section[1]/div[1]/div[1]/div/aside/a/span",
                "xpath2": "/html/body/section[2]/div[1]/div[1]/div/aside/a/span",
            },
            {
                "name": "Meliuz",
                "affiliatedLink": "https://www.meliuz.com.br/i/ref_bae7d6a1?ref_source=2",
                "url": "https://www.meliuz.com.br/desconto/cupom-samsung",
                "xpath": "/html/body/div[3]/div[4]/button",
                "xpath2": "/html/body/div[3]/div[4]/button",
            }
        ]

    def get_response(self, url):
        ua = str(UserAgent().chrome)
        headers = {'User-Agent': ua}
        r = requests.get(url, headers=headers)
        return r
    
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
                cashback_from_coupon = api.get_coupon('cbc460ce-6aa4-4f4f-bce4-79092eba6439')
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

    def coupon_validation(self, description, product):
        return True

    def scrape(self, url, **kwargs):
        ua = str(UserAgent().chrome)
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
        price = None
        # fullPrice = None
        try:
            r = session.get(url)
            r.html.render(sleep=20)
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
    
