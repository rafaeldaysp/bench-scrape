from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os
from lxml import etree

load_dotenv()

MAIN_URL, API_KEY = (os.getenv('MAIN_URL'), os.getenv('API_KEY'))

url = 'https://click.linksynergy.com/deeplink?id=HWP*/f3BEF0&mid=47364&murl=https%3A%2F%2Fwww.lenovo.com%2Fbr%2Fpt%2Flaptops%2Flaptops-legion%2Flegion-5-series%2FLegion-5i-Gen-7-15-inch-Intel%2Fp%2FLEN101G0016%3F'
class Lenovo:
    def __init__(self) -> None:
         self.retailer_id = '87417cba-be9a-49c4-91a2-ed930d7dca2f'
         self.cashbackProviders = [
    {
        "name": "Cuponomia",
        "affiliatedLink": "https://www.cuponomia.com.br/ref/a8a8ec1cba89",
        "url": "https://www.cuponomia.com.br/desconto/lenovo",
        "xpath": "/html/body/section[1]/div[1]/div[1]/div/aside/a/span",
    },
    # {
    #     "name": "Meliuz",
    #     "affiliatedLink": "https://www.meliuz.com.br/i/ref_bae7d6a1?ref_source=2",
    #     "url": "https://www.meliuz.com.br/desconto/cupom-lenovo",
    #     "xpath": "/html/body/div[3]/div[4]/button",
    # },
]

    def coupon_validation(self, description, product):
        return True

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
                cashbackFullLabelArray = soup.find('span', class_='rewardsTag-cashback').text.split(
                    " "
                )

                for label in cashbackFullLabelArray:
                    if "%" in label:
                        cashbackProvider["value"] = float(
                            label[: label.find("%")].replace(",", ".")
                        )
                        if not cashback or cashback["value"] < cashbackProvider["value"]:
                            cashback = cashbackProvider
        except:
            print("erro na busca de cashbacks")
            cashback = None
            
        return cashback

    def scrape(self, url, **kwargs):
        
        price = -2
        site = BeautifulSoup(self.get_response(url).content, 'html.parser')
        try:
            price = float(site.find('dd', {'itemprop': 'price'}).text[3:].replace('.', '').replace(',', '.'))
            stock_msgs = site.findAll('span', {'class': 'stock_message'})
            count = 0
            for msg in stock_msgs:
                if msg.text == 'Esgotado':
                    count += 1
            if count == len(stock_msgs):
                price = -1
        except Exception as e:
            price = -2
            print(e)
        return price, 'Lenovo'

if __name__ == '__main__':
    print(Lenovo().scrape(url, product_id='d1dce1af-14d4-4e9c-b588-cc809e20d8c0'))