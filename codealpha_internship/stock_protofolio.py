import requests
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Alpha Vantage API Key
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

# Function to fetch real-time stock data from Alpha Vantage
def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Time Series (1min)" not in data:
        print(f"Error fetching data for {symbol}. Please check the symbol.")
        return None
    
    # Get the latest data
    latest_time = list(data["Time Series (1min)"].keys())[0]
    latest_close = data["Time Series (1min)"][latest_time]["4. close"]
    
    return float(latest_close)

# Function to get historical stock data (last 5 days)
def get_historical_data(symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        return None
    
    historical_data = []
    for date, stats in data["Time Series (Daily)"].items():
        historical_data.append({
            'Date': date,
            'Close': stats["4. close"]
        })
    
    # Convert to DataFrame for easy viewing
    return pd.DataFrame(historical_data)

# Function to get dividend data (if available)
def get_dividend_data(symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'DIVIDEND_HISTORY',
        'symbol': symbol,
        'apikey': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "dividends" not in data:
        return None
    
    return data["dividends"]

# StockPortfolio class to manage stock investments
class StockPortfolio:
    def __init__(self):
        self.portfolio = {}  # Store stock investments in {symbol: (shares, purchase_price)}

    def add_stock(self, symbol, shares, purchase_price):
        if symbol in self.portfolio:
            self.portfolio[symbol] = (self.portfolio[symbol][0] + shares, purchase_price)
        else:
            self.portfolio[symbol] = (shares, purchase_price)

    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            current_shares, purchase_price = self.portfolio[symbol]
            if current_shares >= shares:
                self.portfolio[symbol] = (current_shares - shares, purchase_price)
            else:
                print(f"Not enough shares to remove. You have {current_shares} shares of {symbol}.")
        else:
            print(f"{symbol} not found in your portfolio.")

    def track_performance(self):
        total_value = 0
        total_investment = 0
        for symbol, (shares, purchase_price) in self.portfolio.items():
            current_price = get_stock_data(symbol)
            if current_price:
                investment_value = shares * current_price
                total_value += investment_value
                total_investment += shares * purchase_price
        return total_investment, total_value

# GUI Application using Tkinter
class StockPortfolioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.portfolio = StockPortfolio()

        # Creating the user interface
        self.create_widgets()

    def create_widgets(self):
        # Labels, entry fields, and buttons
        self.stock_symbol_label = tk.Label(self.root, text="Stock Symbol:")
        self.stock_symbol_label.grid(row=0, column=0, padx=10, pady=10)

        self.stock_symbol_entry = tk.Entry(self.root)
        self.stock_symbol_entry.grid(row=0, column=1, padx=10, pady=10)

        self.shares_label = tk.Label(self.root, text="Shares:")
        self.shares_label.grid(row=1, column=0, padx=10, pady=10)

        self.shares_entry = tk.Entry(self.root)
        self.shares_entry.grid(row=1, column=1, padx=10, pady=10)

        self.purchase_price_label = tk.Label(self.root, text="Purchase Price:")
        self.purchase_price_label.grid(row=2, column=0, padx=10, pady=10)

        self.purchase_price_entry = tk.Entry(self.root)
        self.purchase_price_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Stock", command=self.add_stock)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.remove_button = tk.Button(self.root, text="Remove Stock", command=self.remove_stock)
        self.remove_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.track_button = tk.Button(self.root, text="Track Portfolio", command=self.track_performance)
        self.track_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.history_button = tk.Button(self.root, text="Show Historical Data", command=self.show_historical_data)
        self.history_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.dividend_button = tk.Button(self.root, text="Show Dividend History", command=self.show_dividend_data)
        self.dividend_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_stock(self):
        symbol = self.stock_symbol_entry.get().upper()
        try:
            shares = int(self.shares_entry.get())
            purchase_price = float(self.purchase_price_entry.get())
            self.portfolio.add_stock(symbol, shares, purchase_price)
            messagebox.showinfo("Success", f"Added {shares} shares of {symbol} at ${purchase_price} each.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for shares and price.")

    def remove_stock(self):
        symbol = self.stock_symbol_entry.get().upper()
        try:
            shares = int(self.shares_entry.get())
            self.portfolio.remove_stock(symbol, shares)
            messagebox.showinfo("Success", f"Removed {shares} shares of {symbol}.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of shares.")

    def track_performance(self):
        total_investment, total_value = self.portfolio.track_performance()
        profit_loss = total_value - total_investment
        messagebox.showinfo("Portfolio Performance", f"Total Investment: ${total_investment}\n"
                                                   f"Total Portfolio Value: ${total_value}\n"
                                                   f"Overall Profit/Loss: ${profit_loss}")

    def show_historical_data(self):
        symbol = self.stock_symbol_entry.get().upper()
        historical_data = get_historical_data(symbol)
        if historical_data is not None:
            historical_data_str = historical_data.to_string()
            messagebox.showinfo("Historical Data", historical_data_str)
        else:
            messagebox.showerror("Data Error", "Could not fetch historical data for the given symbol.")

    def show_dividend_data(self):
        symbol = self.stock_symbol_entry.get().upper()
        dividend_data = get_dividend_data(symbol)
        if dividend_data is not None:
            dividends_str = "\n".join([f"Date: {key}, Dividend: {value}" for key, value in dividend_data.items()])
            messagebox.showinfo("Dividend History", dividends_str)
        else:
            messagebox.showerror("Data Error", "No dividend data found for the given symbol.")

# Start the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioGUI(root)
    root.mainloop()
