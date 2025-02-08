import tkinter as tk
from tkinter import ttk
from enums.StockTickerType import InvestType
from PredictEngine import createSignals


def create_ui():
    root = tk.Tk()
    root.title("Investment Signal Generator")
    root.geometry("600x300")  # Set window size to 500x300 pixels

    font = ("Helvetica", 16)

    label_symbol = tk.Label(root, text="Enter Stock Symbol:", font=font)
    label_symbol.grid(row=0, column=0, padx=20, pady=10)

    entry_symbol = tk.Entry(root, font=font)
    entry_symbol.grid(row=0, column=1, padx=20, pady=10)

    label_invest_type = tk.Label(root, text="Select Investment Type:", font=font)
    label_invest_type.grid(row=1, column=0, padx=10, pady=10)

    invest_type_var = tk.StringVar()
    invest_type_dropdown = ttk.Combobox(root, textvariable=invest_type_var, values=[e.name for e in InvestType], font=font)
    invest_type_dropdown.grid(row=1, column=1, padx=20, pady=10)

    def on_submit():
        stock_symbol = entry_symbol.get()
        invest_type = invest_type_var.get()
        if stock_symbol and invest_type:
            createSignals(stock_symbol, InvestType[invest_type].value)
        else:
            print("Please enter both stock symbol and investment type.")

    submit_button = tk.Button(root, text="Generate Signals", command=on_submit, font=font)
    submit_button.grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()