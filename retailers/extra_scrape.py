from requests_html import HTMLSession
import json

class Extra:
    def __init__(self) -> None:
        self.retailer_id = '5e8ca825-31f8-4a0b-a6b6-2a8b0992c8a7'
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
        price, store = [-1, 'Extra']
        try:
            sku = kwargs['sku']
            url_data = f'https://pdp-api.extra.com.br/api/v2/sku/{sku}/price/source/CB?utm_source=undefined&take=undefined&device_type=DESKTOP'
            session2 = HTMLSession(browser_args=["--no-sandbox", "--user-agent=Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.14 Safari/534.24"])
            r2 = session2.get(url_data)
            r2.html.render(sleep=2)
            json_data = json.loads(r2.html.html[r2.html.html.find('{'):r2.html.html.rfind('}')+1])
            r2.close()
            session2.close()
            price, store = [json_data['paymentMethodDiscount']['sellPriceWithDiscount'], json_data['sellers'][0]['name']]
        except Exception as e:
            #print('Scraping Casas Bahia bad request: ', e)
            price = -1
            #print(r.html.html)
            pass
        return price, store

if __name__ == '__main__':
    c = Extra()
    c.scrape('https://www.extra.com.br/notebook-lenovo-amd-ryzen-5-5500u-8gb-256gb-ssd-tela-full-hd-15-6-linux-ideapad-3-82mfs00100-55056427/p/55056427?awc=17629_1684762644_e2b2e347e553a9bb5a6386b5fb47c17f&utm_source=zanox&utm_medium=afiliados&utm_campaign=979245&utm_term=', sku='55056427')
