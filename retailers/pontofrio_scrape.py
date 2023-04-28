from requests_html import HTMLSession
import json

class PontoFio:
    def __init__(self) -> None:
        self.retailer_id = 'b62cec4d-296b-49a1-8db8-64ec4c0e0ec0'
    def coupon_validation(self, description, product):
        if description:
            description = json.loads(description)
            try:
                if product['category']['name'] not in description['category']:
                    return False
            except:
                pass
        return True

    def scrape(self, url, **kwargs):
        price, store = [-1, 'Ponto Frio']
        try:
            sku = kwargs['sku']
            url_data = f'https://pdp-api.pontofrio.com.br/api/v2/sku/{sku}/price/source/CB?utm_source=undefined&take=undefined&device_type=DESKTOP'
            session2 = HTMLSession(browser_args=["--no-sandbox", "--user-agent=Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.14 Safari/534.24"])
            r2 = session2.get(url_data)
            r2.html.render(sleep=2)
            json_data = json.loads(r2.html.html[r2.html.html.find('{'):r2.html.html.rfind('}')+1])
            r2.close()
            session2.close()
            price, store = [json_data['paymentMethodDiscount']['sellPriceWithDiscount'], json_data['sellers'][0]['name']]
        except Exception as e:
            #print('Scraping Casas Bahia bad request: ', e)
            print(e)
            price = -1
            #print(r.html.html)
            pass
        return price, store

if __name__ == '__main__':
    c = PontoFio()
    print(c.scrape('https://www.pontofrio.com.br/Informatica/Notebook/notebook-gamer-dell-g15-a0706-m40p-156-quot-fhd-amd-ryzen-7-6800h-16gb-512gb-ssd-nvidia-rtx-3060-windows-11-1545944459.html', sku='1545944459'))
