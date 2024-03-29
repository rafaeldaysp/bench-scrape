from bs4 import BeautifulSoup
from requests_html import HTMLSession
from fake_useragent import UserAgent

class Avell:
    def __init__(self) -> None:
        self.retailer_id = 'd95b62cd-78c0-465f-8d6e-80151c3c567e'
    def coupon_validation(self, description, product):
        if description:
            try:
                #description = json.loads(description)
                if product['id'] not in description:
                    return False
            except Exception as e:
                pass
        return True
    
    def bestCashbackFinder(self):
        return None

    def scrape(self, url, **kwargs):
        ua = str(UserAgent().chrome)
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
        price = -1
        fullPrice = None
        try:
            r = session.get(url)
            r.html.render(sleep=5)
        except Exception as e:
            print(e)
            price = -2
            session.close()
            return None, None
        try:
            price = float(BeautifulSoup(r.html.raw_html, 'html.parser').find_all('h3', class_='MuiTypography-root MuiTypography-h3')[0].text.replace('.', '').replace(',', '.'))
                        
        except Exception as e:
            print('Erro no produto da Avell', e)
            
        # try:
        #     src = BeautifulSoup(r.html.raw_html, 'html.parser').find('p', class_='MuiTypography-root jss329 MuiTypography-body1')
                        
        #     fullPrice = float(src.text[3:].replace('R$&nbsp;', '').replace('.', '').replace(',', '.'))
        # except:
        #     print('Full price not recognized')
        r.close()
        session.close()
        
        priceWithPixDiscount = price
        
        return priceWithPixDiscount, 'Avell', fullPrice

if __name__ == '__main__':
    avell = Avell()
    print(avell.scrape('https://avell.com.br/avell-a70-hyb-1?utm_source=rakuten&utm_medium=afiliados&utm_campaign=3982103&utm_content=HWP._f3BEF0-rm65jBLB75LDL0q.py.H6Q&ranMID=50236&ranEAID=HWP*%2Ff3BEF0&ranSiteID=HWP._f3BEF0-rm65jBLB75LDL0q.py.H6Q'))