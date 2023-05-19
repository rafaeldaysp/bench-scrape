import json
import re
import requests
from fake_useragent import UserAgent
import re
from requests_html import HTMLSession

class AliExpress:
    def __init__(self) -> None:
        self.retailer_id = '39b03799-2054-4c80-a015-bd1b76358c57'
    def get_response(self, url):
        ua = str(UserAgent().chrome)
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
        headers = {'User-Agent': ua}
        r = session.get(url)
        return r

    def coupon_validation(self, description, product):
        return True

    def scrape(self, url, **kwargs):
        sku_id = kwargs['sku']
        price = -1
        store = None
        ua = str(UserAgent().chrome)
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent="+ua])
        r = session.get(url)
        match = re.search(r'data: ({.+})', r.text).group(1)
        r.close()
        session.close()
        try:
            data = json.loads(match)
        except Exception as e:
            print("_____________________________MUDAR LINK DO PRODUTO ABAIXO__________________________")
            return False, False
        try:
            store = data['storeModule']['storeName']
        except Exception as e:
            return False, False
        price_info = data['skuModule']['skuPriceList']
        qtd_produtos = len(price_info)
        for i in range(0, qtd_produtos):
            if str(price_info[i]['skuId']) == sku_id:
                try:
                    price = price_info[i]['skuVal']['skuActivityAmount']['value']
                except:
                    try:
                        price = price_info[i]['skuVal']['skuAmount']['value']
                    except Exception as e:
                        print(e)
                        print('Erro ao pegar o preço do produto.')
                        return False, False
                if price_info[i]['skuVal']['availQuantity'] == 0:
                    return -1, store
        price_float_value = price
        if price_float_value == -1:
            print('_____________TROCAR SKU DO PRODUTO CUJO SKU ATUAL É: ' + sku_id + ' URL: ' + url)
            return False, False
        try:
            slogan_banner = data['middleBannerModule']['uniformMiddleBanner']['sloganBanner']
            if slogan_banner == 'Preço exclusivo na primeira compra':
                price_float_value += 16
        except: 
            pass
        full_price = price_float_value
        promo_desc = 0
        try:
            promo_15_off_a_cada = data['couponModule']['webCouponInfo']['promotionPanelDTO']['acrossStoreFixedDiscount'][0]['promotionPanelDetailDTOList'][0]['promotionDesc'].replace('(', '').replace(')', '')
            regex = r'\d+'
            values_promo = [int(num) for num in re.findall(regex, promo_15_off_a_cada)]
            promo_desc = int(price_float_value/values_promo[1])*values_promo[0]
            
            if promo_desc > values_promo[2]:
                promo_desc = values_promo[2]
            
        except:
            pass
        price_float_value -= promo_desc
        coupons = []
        coupons_conditions = []
    
        try:
            all_coupons = data['couponModule']['webCouponInfo']['promotionPanelDTO']['shopCoupon'][0]['promotionPanelDetailDTOList']
            for coupon_info in all_coupons:
                coupon_value = float(coupon_info['promotionDesc'][2:].replace(',', '.'))
                coupon_condition_str = coupon_info['promotionDetail']
                index = coupon_condition_str.find('$')
                coupon_condition_value = float(coupon_condition_str[index + 1:].replace(',', '.'))
                coupons.append(coupon_value)
                coupons_conditions.append(coupon_condition_value)
            coupons.sort()
            coupons_conditions.sort()
        except:
            pass
        shop_discounts = []
        shop_discounts_conditions = []
        shop_percent_discount_off = 0
        try:
            all_discounts_list = data['couponModule']['webCouponInfo']['promotionPanelDTO']['storeDiscount'][0]['promotionPanelDetailDTOList']
            for i in range(len(all_discounts_list)):
                all_discounts = all_discounts_list[i]['promotionDetailList']
                if 'Tenha' in all_discounts[0]:
                    for discount in all_discounts:
                        shop_discounts.append(float(discount[discount.find('$') + 1:discount.find(',') + 3].replace(',', '.')))
                        shop_discounts_conditions.append(float(discount[discount.rfind('$') + 1: discount.rfind(',') + 3].replace(',', '.')))
                if 'Compre 1 ' in all_discounts[0]:
                    percent_value = [float(x) for x in all_discounts[0][all_discounts[0].find('1') + 1:all_discounts[0].find('%')].split(' ') if x.isdigit()][0]
                    shop_percent_discount_off = round(price_float_value*percent_value/100, 2)
            shop_discounts.sort()
            shop_discounts_conditions.sort()
        except Exception as e:
            pass
        price_float_value -= shop_percent_discount_off    
        shop_discount_off = 0
        for i in range(len(shop_discounts)):
            try:
                if full_price > shop_discounts_conditions[i]:
                    shop_discount_off = shop_discounts[i]
            except Exception as e:
                pass
        price_float_value -= shop_discount_off 
        shop_coupon_off = 0
        for i in range(len(coupons)):
            try:
                if full_price > coupons_conditions[i]:
                    shop_coupon_off = coupons[i]
            except Exception as e:
                pass
        price_float_value -= shop_coupon_off
        coins_off = 0
        try:
            for promotion in data['priceModule']['promotionSellingPointTags']:
                
                try:  
                    coins_off_str = promotion['elementList'][1]['textContent']
                except Exception as e:
                    pass
                    
            coins_off_value = float(coins_off_str[0:coins_off_str.find('%')])/100
            coins_off = coins_off_value*full_price
        except Exception as e:    
            pass
        price_float_value -= coins_off
        price = round(price_float_value, 2)
    
        # except Exception as e:
        #     #print(f'Erro no scraping do produto: {url}, de sku: {sku_id}')
        #     print(e, url)
        #     price = -2
        return price, store, full_price

if __name__ == '__main__':
    aliexpress = AliExpress()
    print(aliexpress.scrape('https://s.click.aliexpress.com/e/_Dl9PRQD', sku = '12000031047942535'))