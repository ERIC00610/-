import tkinter as tk
import tkinter.font as tkFont
from tkinter.ttk import *
from tkinter import messagebox

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




class requirement_page(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.winfo_toplevel().title("代購策略推薦")
        self.grid()
        self.createwidgets()


    def createwidgets(self):
        fontstyle0 = tkFont.Font(size=16, family="Noto Sans CJK TC Regular")
        fontstyle1 = tkFont.Font(size=20, family="Noto Sans CJK TC Regular")
        # 說明文字
        self.instruction = tk.Label(self, text="輸入可投入的成本及預期報酬，將為您推薦適合的產品", font=fontstyle0)
        self.instruction.grid(row=0, column=0, columnspan=2)
        # 資訊輸入
        self.cost = tk.Label(self, text="可投入的成本：", font=fontstyle1)
        self.cost.grid(row=1, column=0)
        self.cost_entry = tk.Entry(self, width=20, font=fontstyle1)
        self.cost_entry.grid(row=1, column=1)
        self.expected_reward = tk.Label(self, text="預期報酬：", font=fontstyle1)
        self.expected_reward.grid(row=2, column=0, sticky=tk.W)
        self.expected_reward_entry = tk.Entry(self, width=20, font=fontstyle1)
        self.expected_reward_entry.grid(row=2, column=1)
        # 送出按鈕
        self.confirm_btn = tk.Button(text="送出", font=fontstyle1, width=10, command=self.numonly)
        self.confirm_btn.grid(row=3, column=0, columnspan=2)

    # 檢查輸入是否為數字
    def numonly(self):
        try:
            global cost_input
            global expected_reward_input
            cost_input = float(self.cost_entry.get())
            expected_reward_input = float(self.expected_reward_entry.get())
        except:
            self.error_page("請輸入數字")
        else:
            self.master.destroy()
            output_page()

    def error_page(self, error_message):
        self.error = tk.messagebox.showerror(title="錯誤訊息", message=error_message)

class output_page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.winfo_toplevel().title("代購策略推薦")
        self.grid()
        self.resultwidgets()

    def resultwidgets(self):
        fontstyle0 = tkFont.Font(size=16, family="Noto Sans CJK TC Regular")
        fontstyle1 = tkFont.Font(size=20, family="Noto Sans CJK TC Regular")
        # 說明文字
        self.instruction = tk.Label(self, text="根據您的輸入，推薦的產品組合如下：", font=fontstyle1)
        self.instruction.grid(row=0, column=0, columnspan=2)
        # 結果顯示
        outputlist = Returns(expected_reward_input, cost_input)
        if outputlist == []:
            self.hint = tk.Label(self, text="並無符合需求的商品", font=fontstyle1)
            self.hint.grid(row=2, column=0, columnspan=2)
        else:
            self.name = tk.Label(self, text="商品名", font=fontstyle1)
            self.name.grid(row=1, column=0)
            self.num = tk.Label(self, text="所需購買數量", font=fontstyle1)
            self.num.grid(row=1, column=1)
            for i in range(len(outputlist)):
                product_data= list(outputlist[i].values())
                self.showproduct = tk.Label(self, text=product_data[0], font=fontstyle0, bg="white")
                self.showproduct.grid(row=i + 2, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
                self.shownum = tk.Label(self, text=product_data[1], font=fontstyle0, bg="white")
                self.shownum.grid(row=i + 2, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        

page = requirement_page()
page.mainloop()