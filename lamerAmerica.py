import requests
from bs4 import BeautifulSoup
import pandas as pd
re=requests.get('https://www.cremedelamer.com/')
soup_lamer=BeautifulSoup(re.text,'html.parser')
big_table=soup_lamer.findAll('div',{'class':'gnav-links__header'})

All_englishname=[]
All_price=[]
All_url=[]
for table in big_table:
    url_table='https://www.cremedelamer.com'+table.a['href']
    re_table=requests.get(url_table)
    soup_lamertable=BeautifulSoup(re_table.text,'html.parser')
    All_product=soup_lamertable.findAll('div',{'class':'product-brief__header'})
    for product in All_product:
        English_name=product.find('div',{'class':'product-name'}).text
        price=product.find('div',{'class':'product-price'}).text
        url='https://www.cremedelamer.com'+product.find('a')['href']
        All_englishname.append(English_name)
        All_price.append(price)
        All_url.append(url)

data={'商品英文名稱':All_englishname,'商品價格':All_price,'商品連結':All_url}
df=pd.DataFrame(data)
print(df)
df.to_csv('lamerAmerica_Allproductinfo.csv')
