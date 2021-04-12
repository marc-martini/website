# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 18:06:01 2021

@author: marti



"""
from dotenv import load_dotenv
load_dotenv()

import os
import requests
import urllib.parse

def currency(amount):

    dollar = "${:,.2f}".format(amount)

    return dollar

# Function to convert to percentage
def percent(num):

    percent = "{0:.2%}".format(num)

    return percent

def quote_data(user_symbol):

    # parse the symbol for url formatting
    symbol = urllib.parse.quote_plus(user_symbol)

    quote_data = {}
    
    # Full calls for API data

    api_key = os.getenv("API_KEY")
    print(api_key)
    response_chart = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token={}".format(symbol,api_key))
    '''
    earn_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/earnings/?token={}".format(symbol,api_key))

    div_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/dividends/?token={}".format(symbol,api_key))
    '''
    stats_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/stats/dividendYield?token={}".format(symbol,api_key))
        

    # Test calls for API data to configure
    api_key_test = os.getenv("API_KEY_test")

    '''
    response_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/quote/?token={}".format(symbol,api_key_test))
    # Earn chart discontinued
    earn_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/earnings/?token={}".format(symbol,api_key_test))
    stats_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/stats/dividendYield?token={}".format(symbol,api_key_test))
    '''
    div_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/dividends/?token={}".format(symbol,api_key_test))

    print(response_chart)
    print(stats_chart)
    print(div_chart)

    # test data pulled to sure clean return as a dictionary
    try:
        stat = stats_chart.json()
        quote_data["divyield"] = percent(stat)
    except (KeyError, TypeError, ValueError):
        quote_data["divyield"] = "Not Available"

    try:
        div = div_chart.json()
        quote_data["div"] = currency(float(div[0]["amount"]))
    except (KeyError, TypeError, ValueError, IndexError):
        quote_data["div"] = "Not Available"

    try:
        quote_all = response_chart.json()
        # earn = earn_chart.json()


        quote_data.update([
                ("name", quote_all["companyName"]),
                ("price", currency(float(quote_all["latestPrice"]))),
                ("symbol", quote_all["symbol"]),
                ("per" , quote_all["peRatio"]),
                ("mkcap" , currency(quote_all["marketCap"])),
                ("change" , quote_all["change"]),
                ("volume" , quote_all["volume"]),
                ("yearhigh" , quote_all["week52High"]),
                ("yearlow" , quote_all["week52Low"]),
                ("ytdchange" , quote_all["ytdChange"]),
                ("currentmarket" , quote_all["isUSMarketOpen"]),
                ("change_per" , percent(quote_all["changePercent"])),
                ("eps" , None)
                ])

        return quote_data

    except (KeyError, TypeError, ValueError):
        return None
    
    
if __name__ == "__main__":
    user_symbol = input('Stock sym: ')
    quote = quote_data(user_symbol)
    print(quote)
    