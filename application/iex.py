import os
import requests
import urllib.parse

# Function to convert to dollar representaion
def currency(amount):

    dollar = "${:,.2f}".format(amount)

    return dollar

# Function to convert to percentage
def percent(num):

    percent = "{0:.2%}".format(num)

    return percent

# pull historical data for graphs from IEX
def histo_data(user_symbol, rng):

    # parse the symbol for url formatting
    symbol = urllib.parse.quote_plus(user_symbol)

    # data range to string
    chart_range = str(rng)

    # Full calls for API data
'''
    api_key = os.getenv("API_KEY")
    response_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/chart/{}?token={}".format(symbol,chart_range,api_key))
    print(response_chart)
'''

    # Test calls for API data to configure


    api_key_test = os.getenv("API_KEY_test")
    response_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/chart/{}?token={}".format(symbol,chart_range,api_key_test))


    # get the JSON response
    try:
        chart = response_chart.json()
    except:
        return None

    x_val = []
    y_val = []

    if chart_range == '1d':
        ts = 'minute'
    else:
        ts = 'date'

    for row in chart:
        x_val.append(row[ts])
        y_val.append(row["close"])

    return x_val, y_val


def quote_data(user_symbol):

    # parse the symbol for url formatting
    symbol = urllib.parse.quote_plus(user_symbol)

    quote_data = {}

    # Full calls for API data

    api_key = os.getenv("API_KEY")

    response_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/quote?token={}".format(symbol,api_key))
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
        earn = earn_chart.json()


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
                ("eps" , currency(earn["earnings"][0]['actualEPS']))
                ])

        return quote_data

    except (KeyError, TypeError, ValueError):
        return None

def company_data(user_symbol):

    # parse the symbol for url formatting
    symbol = urllib.parse.quote_plus(user_symbol)

    # Full calls for API data

    api_key = os.getenv("API_KEY")

    response_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/company?token={}".format(symbol,api_key))
    '''

    # Test calls for API data to configure
    api_key_test = os.getenv("API_KEY_test")

    response_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/company?token={}".format(symbol,api_key_test))
 '''
    company_all = response_chart.json()

    company_data = {
            "des": company_all["description"],
            "ceo": company_all["CEO"],
            "web": company_all["website"],
            "sect" : company_all["sector"],
            "indus" : company_all["industry"],
            "country" : company_all["country"]
        }

    return company_data

def logo(user_symbol):

    # parse the symbol for url formatting
    symbol = urllib.parse.quote_plus(user_symbol)


    api_key = os.getenv("API_KEY")

    # get the type of data to be pulled from IEX
    response_chart = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/logo?token={}".format(symbol,api_key))

    # api_key_test = os.getenv("API_KEY_test")

    # response_chart = requests.get("https://sandbox.iexapis.com/stable/stock/{}/logo?token={}".format(symbol,api_key_test))

    logo = response_chart.json()

    return logo['url']


def news(user_symbol):

    # parse the symbol for url formatting
    symbol = urllib.parse.quote_plus(user_symbol)


    api_key = os.getenv("API_KEY")

    # get the type of data to be pulled from IEX
    news_response = requests.get("https://cloud-sse.iexapis.com/stable/stock/{}/news?token={}".format(symbol,api_key))

    # api_key_test = os.getenv("API_KEY_test")

    # news_response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/news?token={}".format(symbol,api_key_test))

    news = news_response.json()

    return news
