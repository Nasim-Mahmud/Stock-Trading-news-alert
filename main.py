from twilio.rest import Client
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# API keys
STOCK_API_KEY = "[STOCK_API_KEY]"
NEWS_API_KEY = "[NEWS_API_KEY]"
TWILIO_AUTH_TOKEN = "[TWILIO_AUTH_TOKEN]"

# APIs'
STOCK_API = "https://www.alphavantage.co/query"
NEWS_API = "https://newsapi.org/v2/everything"
TWILIO_ACCOUNT_SID = "[YOUR_TWILIO_ACCOUNT_SID]"

# STEP 1: Use https://www.alphavantage.co
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
dates = list(stock_daily_data)

yesterdays_closing_price = stock_daily_data[dates[1]]["4. close"]
day_before_yesterdays_closing_price = stock_daily_data[dates[2]]["4. close"]

difference = abs(float(yesterdays_closing_price) - float(day_before_yesterdays_closing_price))
difference_in_percentage = (difference / float(yesterdays_closing_price)) * 100
# print(difference_in_percentage)

if difference_in_percentage > 3:
    icon = "🔺"
elif difference_in_percentage < 3:
    icon = "🔻"

if difference_in_percentage > 3 or difference_in_percentage < 3:

    # STEP 2: Use https://newsapi.org

    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "sortBy": "popularity",
        # "category": "business",
    }
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    news_response = requests.get(NEWS_API, params=news_parameters)
    news_response.raise_for_status()

    news_data = news_response.json()["articles"]
    for n in range(0, 3):
        print(news_data[n]["title"])

        # STEP 3: Use https://www.twilio.com Send a separate message with the percentage change and each article's
        # title and description to your phone number.

        excluded_string = ' <a href="https://www.reuters.com/companies/TSLA.O" target="_blank">(TSLA.O)</a>'
        article = f'{STOCK}:{icon}{round(difference_in_percentage, 2)}%' \
                  f'\nHeadline: {news_data[n]["title"]}' \
                  f'\nBrief: {news_data[n]["description"].replace(excluded_string, "")}'
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(body=article, from_="[YOUR_TWILIO_NUMBER]",  # Got the number from Twilio.
                    to="[YOUR_TWILIO_REGISTERED_PHONE_NUMBER]"
                    )
        print(message.status)
        print(article)
