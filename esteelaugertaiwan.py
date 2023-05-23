import requests
from bs4 import BeautifulSoup
import pandas as pd
esteelurl='https://www.esteelauder.com.tw/products/1799/product-catalog/bestsellers'
user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
headers={'User-Agent':user_agent}
re=requests.get(esteelurl,headers=headers)
re.encoding='UTF-8'
soup_esteelanuderskincare=BeautifulSoup(re.text,'html.parser')

all_product=soup_esteelanuderskincare.findAll('div',{'class':'sc-qcrOD lgHeMB elc-product-brief js-product-brief'})

for product in all_product:
    English_name=product.find('h2',{'data-test-id':'product_name'}).text
    print(English_name)
