import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

MAIN_URL, API_KEY = (os.getenv('MAIN_URL'), os.getenv('API_KEY'))

headers = {'api-key': API_KEY}

def get_coupons(retailer_id):
    try:
        coupons = json.loads(requests.get(MAIN_URL + '/retailers/' + retailer_id + '/coupons', headers=headers).text)
        return coupons
    except:
        return [] 

def get_product_retailers(product_id):
   return json.loads(requests.get(MAIN_URL + '/products/' + product_id + '/retailers', headers=headers).text)

def update_product_retailers(product_id, retailer_id, data):
    return requests.patch(MAIN_URL + '/products/' + product_id + '/retailers/' + retailer_id, json=data, headers=headers)

def get_products():
    return json.loads(requests.get(MAIN_URL + '/products', headers=headers).text)

def get_coupon(coupon_id):
    return json.loads(requests.get(MAIN_URL + '/coupons/' + coupon_id, headers=headers).text)

def get_retailer_products(retailer_id):
    try:
        products = json.loads(requests.get(MAIN_URL + '/retailers/' + retailer_id + '/products', headers=headers).text)
        return products
    except:
        return []

def create_coupon(data):
    return requests.post(MAIN_URL + '/coupons', headers=headers, json=data)

def delete_coupon(coupon_id):
    return requests.delete(MAIN_URL + '/coupons/' + coupon_id, headers=headers)

def get_retailers():
    return json.loads(requests.get(MAIN_URL + '/retailers', headers=headers).text)