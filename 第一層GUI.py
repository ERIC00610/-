import tkinter as tk
import tkinter.font as tkFont
from tkinter.ttk import *
from tkinter import messagebox

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
        self.cost_entry = tk.Entry(self, width=30, font=fontstyle1)
        self.cost_entry.grid(row=1, column=1)
        self.expected_reward = tk.Label(self, text="預期報酬：", font=fontstyle1)
        self.expected_reward.grid(row=2, column=0, sticky=tk.W)
        self.expected_reward_entry = tk.Entry(self, width=30, font=fontstyle1)
        self.expected_reward_entry.grid(row=2, column=1)
        # 送出按鈕
        self.confirm_btn = tk.Button(text="送出", font=fontstyle1, width=10, command=self.numonly)
        self.confirm_btn.grid(row=3, column=0, columnspan=2)

    # 檢查輸入是否為數字
    def numonly(self):
        try:
            float(self.cost_entry.get())
            float(self.expected_reward_entry.get())
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
        self.instruction = tk.Label(self, text="根據您的輸入，推薦的產品組合如下：", font=fontstyle0)
        self.instruction.grid(row=0, column=0, columnspan=2)

page = requirement_page()
page.mainloop()