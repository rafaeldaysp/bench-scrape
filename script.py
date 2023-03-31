from api import api


def run(product, Retailer):
    retailer_id = Retailer.retailer_id
    scrape = Retailer.scrape
    coupon_validation = Retailer.coupon_validation
    data = {}
    price, store, *full_price = scrape(product['html_url'], product_id = product['id'], sku = product['dummy'], retailer_id = retailer_id)
    if not price:
        print('Erro em: ', product['title'])
        return
    if not full_price:
        full_price = price
    if price > 0:
        data['available'] = True
        data['price'] = int(price*100)
        data['store'] = store
        all_coupons = api.get_coupons(retailer_id)
        possible_coupons = []
        for i in range(len(all_coupons)):
            if coupon_validation(all_coupons[i]['description'], product):
                    possible_coupons.append(all_coupons[i])
        best_discount_amount = 0
        best_coupon_id = None
        for coupon in possible_coupons:
            if not coupon['minimum_spend']:
                coupon['minimum_spend'] = 0
            if coupon['retailer_id'] == retailer_id and coupon['minimum_spend'] <= full_price[0] and coupon['available']:
                discount = coupon['discount']
                if '%' in discount:
                    discount = float(discount[:-1])*full_price[0]/100
                else:
                    discount = float(discount)
                if discount > best_discount_amount:
                    best_coupon_id = coupon['id']
                    best_discount_amount = discount
        data['coupon_id'] = best_coupon_id
        data['price'] = int((price - best_discount_amount)*100)
        if data['price'] != product['price']:
            response = api.update_product_retailers(product['id'], retailer_id, data)
    else:
        data['available'] = False
        response = api.update_product_retailers(product['id'], retailer_id, data)
    
    print(product['title'], data)