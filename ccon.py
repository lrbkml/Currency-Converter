#!/usr/bin/env python
# coding: utf-8

# In[6]:


# # Python Project on Currency Converter

import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

btnState = False


class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

            # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter = converter

        # loading the switch images:
        self.onImg = PhotoImage(file=r"crc.png")
        self.offImg = PhotoImage(file=r"crc.png")

        # setting the geometry and background color and setting the dark mode button in off state
        self.geometry("500x300")
        self.config(bg="#CECCBE")

        # Label
        self.intro_label = Label(self, text='Welcome to Real Time Currency Convertor', fg='blue', relief=tk.RAISED,
                                 borderwidth=3)
        self.intro_label.config(font=('Courier', 15, 'bold'))

        self.date_label = Label(self,
                                text=f"1 Indian Rupee equals = {self.currency_converter.convert('INR', 'USD', 1)} USD \n Date : {self.currency_converter.data['date']}",
                                relief=tk.GROOVE, borderwidth=5)
        # switch widget:
        self.btn = tk.Button(self, text="OFF", borderwidth=0, command=self.switch, bg="#CECCBE",
                             activebackground="#CECCBE")

        self.btn.config(image=self.offImg)
        self.intro_label.place(x=10, y=20)
        self.date_label.place(x=160, y=70)
        self.btn.place(x=390, y=70)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self, bd=3, relief=tk.RIDGE, justify=tk.CENTER, validate='key', validatecommand=valid)
        self.converted_amount_field_label = Label(self, text='', fg='black', bg='white', relief=tk.RIDGE,
                                                  justify=tk.CENTER, width=17, borderwidth=3)

        # dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("INR")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")  # default value

        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.currency_converter.currencies.keys()), font=font,
                                                   state='readonly', width=12, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.currency_converter.currencies.keys()), font=font,
                                                 state='readonly', width=12, justify=tk.CENTER)

        # placing
        self.from_currency_dropdown.place(x=30, y=120)
        self.amount_field.place(x=36, y=150)
        self.to_currency_dropdown.place(x=340, y=120)
        # self.converted_amount_field.place(x = 346, y = 150)
        self.converted_amount_field_label.place(x=346, y=150)

        # Convert button
        self.convert_button = Button(self, text="Convert", fg="black", command=self.perform)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x=225, y=135)

    def switch(self):
        global btnState
        if btnState:
            self.btn.config(image=self.offImg, bg="#CECCBE", activebackground="#CECCBE")
            self.config(bg="#CECCBE")
            # txt.config(text="Dark Mode: OFF", bg="#CECCBE")
            btnState = False
        else:
            self.btn.config(image=self.onImg, bg="#2B2B2B", activebackground="#2B2B2B")
            self.config(bg="#2B2B2B")
            # txt.config(text="Dark Mode: ON", bg="#2B2B2B")
            btnState = True

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text=str(converted_amount))

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()

#In[ ]:


# In[ ]:




