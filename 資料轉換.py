import csv
import ast
# 讀取美國官網檔案
fn = '2_lamerAm_info.csv'
file_am = []
with open(fn) as csvfile:
    csvdictreader = csv.DictReader(csvfile)
    for row in csvdictreader:
        file_am.append(row)
# print(file_am)

# 讀取台灣官網檔案
fn = '2_lamerTw_info.csv'
file_tw = []
with open(fn) as csvfile:
    csvdictreader = csv.DictReader(csvfile)
    for row in csvdictreader:
        file_tw.append(row)
# print(file_tw)

#抓取匯率
import requests
from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=%E7%BE%8E%E9%87%91'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
resp = requests.get(url, headers={
    'user-agent': user_agent
})
soup = BeautifulSoup(resp.text, 'html.parser')
ele = soup.find('span', class_='DFlfde SwHCTb')
exchange_rate = float(ele.text)

# 資料處理

# 美國官網價錢轉換成台幣並製作兩邊網站共有商品的列表

final_product_lst = []
identifier = set()
for product_tw in file_tw:
    for product_am in file_am:
        if product_tw['商品英文名稱'] == product_am['商品英文名稱'] and product_tw['商品英文名稱'] not in identifier:
            product_tw['商品國外價格'] = product_am['商品價格']
            final_product_lst.append(product_tw)
            identifier.add(product_tw['商品英文名稱'])
#把價格換成int

for product in final_product_lst:
    product['商品價格'] = ast.literal_eval(product['商品價格'])
    product['商品國外價格'] = ast.literal_eval(product['商品國外價格'])
        
# 
for product in final_product_lst:
    return_rate = []
    returns = 0
    if type(product['商品價格'][0]) == int and type(product['商品國外價格'][0]) == int:
        returns = (product['商品價格'][0] - (product['商品國外價格'][0] * exchange_rate)) / (product['商品國外價格'][0] * exchange_rate)
        return_rate.append(returns)
        product['報酬率'] = return_rate
    if type(product['商品價格'][0]) == int and type(product['商品國外價格'][0]) == list:
        return_rate = 0
        price = 0
        for i in product['商品國外價格']:
            returns = (product['商品價格'][0] - (i[1] * exchange_rate)) / (i[1] * exchange_rate)
            if returns > return_rate:
                return_rate = returns
                price = i[1] * exchange_rate
        product['報酬率'] = return_rate
        product['商品國外價格'] = [price]
    if type(product['商品價格'][0]) == list and type(product['商品國外價格'][0]) == list:
        return_rate = []
        returns = 0
        for i in product['商品價格']:
            pro = []
            pro.append(i[0])
            for j in product['商品國外價格']:
                if abs(int(i[0][:-2]) - j[0]) < 5:
                    returns = (i[1] - j[1] * exchange_rate) / (j[1] * exchange_rate)
                    pro.append(returns)
            return_rate.append(pro)
            product['報酬率'] = return_rate
        
def Returns(exp_returns, cost):
    return_lst = []
    exp_returns = int(exp_returns)
    cost = int(cost)
    for i in range(len(final_product_lst)):
        return_pro = {}
        try:
            if type(final_product_lst[i]['報酬率']) == float:
                if (final_product_lst[i]['報酬率'] * cost >= exp_returns) and (cost > final_product_lst[i]['商品國外價格'][0]):
                    return_pro['商品名'] = final_product_lst[i]['商品中文名稱']
                    return_pro['所需購買數量'] = cost // final_product_lst[i]['商品國外價格'][0]
                    return_lst.append(return_pro)
        except KeyError:
            pass
    return return_lst

print(Returns(10000,100000))
