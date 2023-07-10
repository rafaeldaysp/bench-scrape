import sys
from retailers import aliexpress_scrape, acer_scrape, asus_scrape, amazon_scrape, avell_scrape, carrefour_scrape, casasbahia_scrape, extra_scrape, girafa_scrape, kabum_scrape, lenovo_scrape, magalu_af_scrape, nave_scrape, fastshop_scrape, dell_scrape, pontofrio_scrape
from api import api
import concurrent.futures
import script
from fake_useragent import UserAgent
from requests_html import HTMLSession

def multithreadingTrigger(Retailer):
    products = api.get_retailer_products(Retailer.retailer_id)
    cashback = Retailer.bestCashbackFinder()
    
    for product in products:
        # try:
            print("x--------------------------------------------------------------------------------------------x")
            print(product['title'] + '\n')
            script.run(product, Retailer, cashback)
        # except Exception as e:
        #     print(e)
    #concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products), [cashback]*len(products)) 
    
def javascriptRenderTrigger(Retailer):
    ua = str(UserAgent().chrome)
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
    session.get('https://google.com/').html.render()
    session.close()
    
    products = api.get_retailer_products(Retailer.retailer_id)
    for product in products:
        script.run(product, Retailer)

if __name__ == '__main__':
    
        if sys.argv[1] == '--aliexpress':
            multithreadingTrigger(aliexpress_scrape.AliExpress())
        if sys.argv[1] == '--acer':
            multithreadingTrigger(acer_scrape.Acer())
        if sys.argv[1] == '--amazon':
            javascriptRenderTrigger(amazon_scrape.Amazon())
        if sys.argv[1] == '--avell':
            javascriptRenderTrigger(avell_scrape.Avell())
        if sys.argv[1] == '--carrefour':
            multithreadingTrigger(carrefour_scrape.Carrefour())
        if sys.argv[1] == '--casasbahia':
            javascriptRenderTrigger(casasbahia_scrape.CasasBahia())
        if sys.argv[1] == '--girafa':
            javascriptRenderTrigger(girafa_scrape.Girafa())
        if sys.argv[1] == '--kabum':
            multithreadingTrigger(kabum_scrape.Kabum())
        if sys.argv[1] == '--lenovo':
            multithreadingTrigger(lenovo_scrape.Lenovo())
        if sys.argv[1] == '--magaluparceiro':
           multithreadingTrigger(magalu_af_scrape.MagaluParceiro())
        if sys.argv[1] == '--nave':
            javascriptRenderTrigger(nave_scrape.Nave())
        if sys.argv[1] == '--dell':
            multithreadingTrigger(dell_scrape.Dell())
        if sys.argv[1] == '--fastshop':
            multithreadingTrigger(fastshop_scrape.Fastshop())
        if sys.argv[1] == '--pontofrio':
            javascriptRenderTrigger(pontofrio_scrape.PontoFio())
        if sys.argv[1] == '--extra':
            javascriptRenderTrigger(extra_scrape.Extra())
        if sys.argv[1] == '--asus':
            javascriptRenderTrigger(asus_scrape.Asus())
    