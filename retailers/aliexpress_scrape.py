import json
import re
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class AliExpress:
    def __init__(self) -> None:
        self.retailer_id = '39b03799-2054-4c80-a015-bd1b76358c57'
    def get_response(self, url):
        ua = str(UserAgent().chrome)
        headers = {'User-Agent': ua}
        r = requests.get(url, headers=headers)
        return r

    def coupon_validation(self, description, product):
        return True

    def scrape(self, url, **kwargs):
        sku_id = kwargs['sku']
        price = -1
        store = None
        r = self.get_response(url)
        match = re.search(r'data: ({.+})', r.text).group(1)
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
                    price = price_info[i]['skuVal']['skuActivityAmount']['formatedAmount']
                except:
                    try:
                        price = price_info[i]['skuVal']['skuAmount']['formatedAmount']
                    except Exception as e:
                        print(e)
                        print('Erro ao pegar o preço do produto.')
                        return False, False
                if price_info[i]['skuVal']['availQuantity'] == 0:
                    return -1, store
        price_float_value = float(price[3:].replace(',', ''))
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
            values_promo = [int(s) for s in promo_15_off_a_cada.split() if s.isdigit()]
            promo_desc = int(price_float_value/values_promo[1])*values_promo[0]
            if promo_desc > values_promo[2]:
                promo_desc = values_promo[2]
            price_float_value -= promo_desc
        except:
            pass
        
        coupons = []
        coupons_conditions = []
    
        try:
            all_coupons = data['couponModule']['webCouponInfo']['promotionPanelDTO']['shopCoupon'][0]['promotionPanelDetailDTOList']
            for coupon_info in all_coupons:
                coupon_value = float(coupon_info['promotionDesc'][3:].replace(',', '.'))
                coupon_condition_str = coupon_info['promotionDetail']
                index = coupon_condition_str.find('$')
                coupon_condition_value = float(coupon_condition_str[index + 2:].replace(',', '.'))
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
                        shop_discounts.append(float(discount[discount.find('$') + 2:discount.find('.') + 3]))
                        shop_discounts_conditions.append(float(discount[discount.rfind('$') + 2: discount.rfind('.') + 3]))
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
                if price_float_value > shop_discounts_conditions[i]:
                    shop_discount_off = shop_discounts[i]
            except Exception as e:
                pass
        price_float_value -= shop_discount_off 
        shop_coupon_off = 0
        for i in range(len(coupons)):
            try:
                if price_float_value > coupons_conditions[i]:
                    shop_coupon_off = coupons[i]
            except Exception as e:
                pass
        price_float_value -= shop_coupon_off
        coins_off = 0
        try:
            coins_off_str = data['priceModule']['promotionSellingPointTags'][0]['elementList'][1]['textContent']
            coins_off_value = float(coins_off_str[0:coins_off_str.find('%')])/100
            coins_off = coins_off_value*price_float_value
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
    print(aliexpress.scrape('https://pt.aliexpress.com/item/1005005071707765.html?aff_fcid=3109c7e8dfe64b58b1ae6113b3259d4d-1682945649078-04263-_DEvYzy1&tt=CPS_NORMAL&aff_fsk=_DEvYzy1&aff_platform=shareComponent-detail&sk=_DEvYzy1&aff_trace_key=3109c7e8dfe64b58b1ae6113b3259d4d-1682945649078-04263-_DEvYzy1&terminal_id=4ba0548134764b7786731ef60a8d595b&afSmartRedirect=y', sku = '12000031525007843'))