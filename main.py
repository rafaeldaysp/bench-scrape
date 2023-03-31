import sys
from retailers import aliexpress_scrape, acer_scrape, amazon_scrape, avell_scrape, carrefour_scrape, casasbahia_scrape, girafa_scrape, kabum_scrape, lenovo_scrape, magalu_af_scrape, nave_scrape
from api import api
import concurrent.futures
import script
from fake_useragent import UserAgent
from requests_html import HTMLSession

def aliexpressTrigger():
    Retailer = aliexpress_scrape.AliExpress()
    products = api.get_retailer_products(Retailer.retailer_id)
    # for product in products:
    #     script.run(product, Retailer)
    concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))
    
def acerTrigger():
    Retailer = acer_scrape.Acer()
    products = api.get_retailer_products(Retailer.retailer_id)
    # for product in products:
    #     script.run(product, Retailer)
    concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))

def amazonTrigger():
    ua = UserAgent().chrome
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
    session.get('https://google.com/').html.render()
    session.close()
    
    Retailer = amazon_scrape.Amazon()
    products = api.get_retailer_products(Retailer.retailer_id)
    for product in products:
        script.run(product, Retailer)
    

def avellTrigger():
    ua = UserAgent().chrome
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
    session.get('https://google.com/').html.render()
    session.close()
    
    Retailer = avell_scrape.Avell()
    products = api.get_retailer_products(Retailer.retailer_id)
    for product in products:
        script.run(product, Retailer)

def carrefourTrigger():
    Retailer = carrefour_scrape.Carrefour()
    products = api.get_retailer_products(Retailer.retailer_id)
    # for product in products:
    #     script.run(product, Retailer)
    concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))

def casasbahiaTrigger():
    ua = UserAgent().chrome
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
    session.get('https://google.com/').html.render()
    session.close()
    
    Retailer = casasbahia_scrape.CasasBahia()
    products = api.get_retailer_products(Retailer.retailer_id)
    for product in products:
        script.run(product, Retailer)

def girafaTrigger():
    ua = UserAgent().chrome
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
    session.get('https://google.com/').html.render()
    session.close()
    
    Retailer = girafa_scrape.Girafa()
    products = api.get_retailer_products(Retailer.retailer_id)
    for product in products:
        script.run(product, Retailer)

def kabumTrigger():
    Retailer = kabum_scrape.Kabum()
    products = api.get_retailer_products(Retailer.retailer_id)
    for product in products:
        script.run(product, Retailer)
    #concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))

def lenovoTrigger():
    Retailer = lenovo_scrape.Lenovo()
    products = api.get_retailer_products(Retailer.retailer_id)
    # for product in products:
    #     script.run(product, Retailer)
    concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))

def magaluparceiroTrigger():
    Retailer = magalu_af_scrape.MagaluParceiro()
    products = api.get_retailer_products(Retailer.retailer_id)
    # for product in products:
    #     script.run(product, Retailer)
    concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))

def naveTrigger():
    Retailer = nave_scrape.Nave()
    products = api.get_retailer_products(Retailer.retailer_id)
    # for product in products:
    #     script.run(product, Retailer)
    concurrent.futures.ThreadPoolExecutor().map(script.run, products, [Retailer]*len(products))

if __name__ == '__main__':
    try:
        if sys.argv[1] == '--aliexpress':
            aliexpressTrigger()
        if sys.argv[1] == '--acer':
            acerTrigger()
        if sys.argv[1] == '--amazon':
            amazonTrigger()
        if sys.argv[1] == '--avell':
            avellTrigger()
        if sys.argv[1] == '--carrefour':
            carrefourTrigger()
        if sys.argv[1] == '--casasbahia':
            casasbahiaTrigger()
        if sys.argv[1] == '--girafa':
            girafaTrigger()
        if sys.argv[1] == '--kabum':
            kabumTrigger()
        if sys.argv[1] == '--lenovo':
            lenovoTrigger()
        if sys.argv[1] == '--magaluparceiro':
            magaluparceiroTrigger()
        if sys.argv[1] == '--nave':
            naveTrigger()
    except:
        print('Retailer name required. Ex: --retailer')
    