import requests
from bs4 import BeautifulSoup
import pandas as pd
re=requests.get('https://www.esteelauder.com/products/1799/product-catalog/bestsellers')
soup_esteelanuderskincare=BeautifulSoup(re.text,'html.parser')

all_product=soup_esteelanuderskincare.findAll('div',{'class':'flex flex-col flex-1 pl-[10px] pt-[10px] md:pl-0 md:pt-0 md:mr-[10px]'})


All_englishname=[]
All_price=[]
All_url=[]

for product in all_product:
    English_name=product.find('a',{'class':'cursor-pointer'}).text
    price=product.find('div',{'class':'font-bold leading-[1.25rem] product-price font-akzidenzgrotesk text-15px text-navy'}).text
    url=product.find('a')['href']
    All_englishname.append(English_name)
    All_price.append(price)
    All_url.append(url)
data={'商品英文名稱':All_englishname,'商品價格':All_price,'商品連結':All_url}
df=pd.DataFrame(data)
print(df)