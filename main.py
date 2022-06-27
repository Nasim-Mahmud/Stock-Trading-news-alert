import requests
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "2GH6SW5RD8YAW16J"
STOCK_API = "https://www.alphavantage.co/query"

NEWS_API = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "505436ebfeac44938deadd3fc0db0d53"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_API, params=stock_parameters)
response.raise_for_status()

stock_data = response.json()
stock_daily_data = stock_data["Time Series (Daily)"]
dates  = list(stock_daily_data)

yesterdays_closing_price = stock_daily_data[dates[1]]["4. close"]
day_before_yesterdays_closing_price = stock_daily_data[dates[2]]["4. close"]

print(yesterdays_closing_price)
print(day_before_yesterdays_closing_price)

difference = abs(float(yesterdays_closing_price) - float(day_before_yesterdays_closing_price))
difference_in_percentage = (difference / float(yesterdays_closing_price)) * 100
print(difference_in_percentage)

if difference_in_percentage > 3:
    print("Get news")


## STEP 2: Use https://newsapi.org
news_parameters = {
    "apiKey": NEWS_API_KEY,
    "q" : COMPANY_NAME,
    "sortBy": "popularity",
    # "category": "business",
}
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_response = requests.get(NEWS_API, params=news_parameters)
news_response.raise_for_status()

news_data = news_response.json()
print(news_data)
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
