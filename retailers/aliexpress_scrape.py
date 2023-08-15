import json
import re
import requests
from fake_useragent import UserAgent
import re

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

    def bestCashbackFinder(self):
        return None

    def scrape(self, url, **kwargs):
        sku_id = kwargs['sku']
        price = -1
        store = None
        r = self.get_response(url)
        
        try:
            match = re.search(r'data: ({.+})', r.text).group(1)
            data = json.loads(match)
        except Exception as e:
            print("_____________________________MUDAR LINK DO PRODUTO ABAIXO__________________________")
            return False, False
        try:
            store = 'AliExpress'#data['storeModule']['storeName']
        except Exception as e:
            print(e)
            return False, False
        price_info = data['priceComponent']['skuPriceList']
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
            slogan_banner = data['simpleBannerComponent']['simpleBannerInfo']['bannerType']
            if slogan_banner == 'platform_newer':
                price_float_value += 15
        except: 
            pass
        full_price = price_float_value
        print('Preço total: ', full_price)
        promo_desc = 0
        try:
            promo_15_off_a_cada = data['webCouponInfoComponent']['promotionPanelDTO']['acrossStoreFixedDiscount'][0]['promotionPanelDetailDTOList'][0]['promotionDesc'].replace('(', '').replace(')', '')
            regex = r'\d+'
            values_promo = [int(num) for num in re.findall(regex, promo_15_off_a_cada)]
            promo_desc = int(price_float_value/values_promo[1])*values_promo[0]
            
            if promo_desc > values_promo[2]:
                promo_desc = values_promo[2]
            
        except:
            pass
        price_float_value -= promo_desc
        print('Desconto "x a cada y gastos...": ', promo_desc)
        coupons = []
        coupons_conditions = []
    
        try:
            all_coupons = data['webCouponInfoComponent']['promotionPanelDTO']['shopCoupon'][0]['promotionPanelDetailDTOList']
            for coupon_info in all_coupons:
                coupon_value = float(coupon_info['promotionDesc'][2:].replace(',', '.'))
                coupon_condition_str = coupon_info['promotionDetail']
                
                index = coupon_condition_str.find('$')
                coupon_condition_value = float(coupon_condition_str[index + 1:].replace('.', '').replace(',', '.'))
                coupons.append(coupon_value)
                coupons_conditions.append(coupon_condition_value)
            coupons.sort()
            coupons_conditions.sort()
        except Exception as e:
            print(e)
        shop_discounts = []
        shop_discounts_conditions = []
        shop_percent_discount_off = 0
        try:
            all_discounts_list = data['webCouponInfoComponent']['promotionPanelDTO']['storeDiscount'][0]['promotionPanelDetailDTOList']
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
        print("Desconto percentual do vendedor: ", shop_percent_discount_off)
        shop_discount_off = 0
        for i in range(len(shop_discounts)):
            try:
                if full_price > shop_discounts_conditions[i]:
                    shop_discount_off = shop_discounts[i]
            except Exception as e:
                pass
        price_float_value -= shop_discount_off
        print("Desconto líquido do vendedor: ", shop_discount_off)
        shop_coupon_off = 0
        for i in range(len(coupons)):
            try:
                if full_price > coupons_conditions[i]:
                    shop_coupon_off = coupons[i]
            except Exception as e:
                pass
        price_float_value -= shop_coupon_off
        print("Desconto do cupom do vendedor: ", shop_coupon_off)
        coins_off = 0
        try:
            for promotion in data['productTagComponent']['promotionTags']:
                
                try:  
                    coins_off_str = promotion['elementList'][1]['textContent']
                except Exception as e:
                    pass
                    
            coins_off_value = float(coins_off_str[0:coins_off_str.find('%')])/100
            coins_off = coins_off_value*price_float_value
        except Exception as e:    
            pass
        price_float_value -= coins_off
        print("Desconto das moedas: ", coins_off)
        price = round(price_float_value, 2)
        full_price = price
        print("\nPreço final: ", price, '\n')
    
        # except Exception as e:
        #     #print(f'Erro no scraping do produto: {url}, de sku: {sku_id}')
        #     print(e, url)
        #     price = -2
        return price, store, full_price

if __name__ == '__main__':
    aliexpress = AliExpress()
    print(aliexpress.scrape('https://pt.aliexpress.com/item/1005005222129894.html?pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000032267205536%22%7D&&scm=1007.25281.317569.0&scm_id=1007.25281.317569.0&scm-url=1007.25281.317569.0&pvid=e7cc58e1-2ce8-4d60-97f9-4a68155fba89&utparam=%257B%2522process_id%2522%253A%2522standard-item-process-1%2522%252C%2522x_object_type%2522%253A%2522product%2522%252C%2522pvid%2522%253A%2522e7cc58e1-2ce8-4d60-97f9-4a68155fba89%2522%252C%2522belongs%2522%253A%255B%257B%2522floor_id%2522%253A%252239165085%2522%252C%2522id%2522%253A%252232223966%2522%252C%2522type%2522%253A%2522dataset%2522%257D%252C%257B%2522id_list%2522%253A%255B%25221000475524%2522%255D%252C%2522type%2522%253A%2522gbrain%2522%257D%255D%252C%2522pageSize%2522%253A%25226%2522%252C%2522language%2522%253A%2522pt%2522%252C%2522scm%2522%253A%25221007.25281.317569.0%2522%252C%2522countryId%2522%253A%2522BR%2522%252C%2522scene%2522%253A%2522TopSelection-Waterfall%2522%252C%2522tpp_buckets%2522%253A%252221669%25230%2523265320%252343_21669%25234190%252319167%2523903_15281%25230%2523317569%25230%2522%252C%2522x_object_id%2522%253A%25221005005222129894%2522%257D&pdp_npi=3%40dis%21BRL%21R%24%20282%2C29%21R%24%20112%2C04%21%21%21%21%21%402101f49916921299852112003e565e%2112000032267205536%21gdf%21%21&spm=a2g0o.tm1000001240.5535070930.d1&aecmd=true', sku = '12000032267205536'))