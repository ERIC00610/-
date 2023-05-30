import requests
from bs4 import BeautifulSoup
import pandas as pd
re=requests.get('https://www.lamer.com.tw/#')
soup_lamer=BeautifulSoup(re.text,'html.parser')
big_table=soup_lamer.findAll('a',{'class':'button site-header__subnav-button-link'})

All_englishname=[]
All_chinesename=[]
All_price=[]
All_url=[]
avoid=[' 奇蹟煥采氣墊粉霜SPF20',' 潤澤無瑕持妝粉底液SPF20',' 完美輕蜜粉',' 粉底刷',' 蜜粉刷']
for table in big_table:
    url_table='https://www.lamer.com.tw'+table['href']
    re_table=requests.get(url_table)
    soup_lamertable=BeautifulSoup(re_table.text,'html.parser')
    All_product=soup_lamertable.findAll('div',{'class':'product-brief__header'})
    category=table.text
    if category ==' 全部底妝系列商品 ':
        for product in All_product:
            English_name=product.find('div',{'class':'product__subline'}).text
            Chinese_name=product.find('div',{'class':'product-name'}).text
            price=product.find('div',{'class':'product-price'}).text
            url='https://www.lamer.com.tw'+product.find('a')['href']
            All_englishname.append(English_name)
            All_chinesename.append(Chinese_name)
            All_price.append(price)
            All_url.append(url)
    else:
        for product in All_product:
            English_name=product.find('div',{'class':'product-name'}).text
            Chinese_name=product.find('div',{'class':'product__subline'}).text
            price=product.find('div',{'class':'product-price'}).text
            url='https://www.lamer.com.tw'+product.find('a')['href']
            print(English_name)
            if English_name in avoid:
                continue
            else:
                All_englishname.append(English_name)
                All_chinesename.append(Chinese_name)
                All_price.append(price)
                All_url.append(url)
    
data={'商品英文名稱':All_englishname,'商品中文名稱':All_chinesename,'商品價格':All_price,'商品連結':All_url}
df=pd.DataFrame(data)
print(df)
df.to_csv('lamerTaiwan_Allproductinfo.csv')