import requests
from config import *

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ENTER_YOUR_NUMBER = input("Enter your phone number including country code: ")
AV_endpoint = AV_endpoint
NEWS_ENDPOINT = NEWS_ENDPOINT

AV_API = AV_API
NEWS_API = NEWS_API
ACCOUNT_SID = ACCOUNT_SID
TWILIO_API_TOKEN = TWILIO_API_TOKEN

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameters = {"function": "TIME_SERIES_DAILY_ADJUSTED",
              "symbol": STOCK,
              "apikey": AV_API
              }

response = requests.get(AV_endpoint, params=stock_parameters)
response.raise_for_status()
daily_stocks = response.json()

yesterday = list(daily_stocks["Time Series (Daily)"].keys())[0]
day_before = list(daily_stocks["Time Series (Daily)"].keys())[1]

yesterday_price = daily_stocks["Time Series (Daily)"][f"{yesterday}"]["4. close"]
day_before_price = daily_stocks["Time Series (Daily)"][f"{day_before}"]["4. close"]
delta_percent = round((float(yesterday_price) - float(day_before_price)) / float(yesterday_price) * 100)
if delta_percent >= 0:
    if delta_percent == 0:
        TSLA = "Price stayed the same"
    else:
        TSLA = f"🔺 {delta_percent}%"
else:
    TSLA = f"🔻 {abs(delta_percent)}%"

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

if abs(delta_percent) > 4:
    news_params = {"q": "Tesla",
                   "apiKey": NEWS_API
                   }

    news = requests.get(NEWS_ENDPOINT, params=news_params)
    news.raise_for_status()
    top_headlines = news.json()
    top_three = top_headlines["articles"][:3]

    for x in range(0, 3):
        try:
            headline = top_three[x]["title"]
            description = top_three[x]["description"]
            URL = top_three[x]["url"]
            print(f"TSLA: {TSLA}\nHeadline: {headline} \nDescription: {description} \nURL: {URL} ")
        except IndexError:
            print("No more Articles for now")
            break
        client = Client(ACCOUNT_SID, TWILIO_API_TOKEN)
        message = client.messages \
                        .create(
                             body=f"TSLA: {TSLA}\nHeadline: {headline} \nDescription: {description} \nURL: {URL}",
                             from_='+16205089044',
                             to='ENTER_YOUR_NUMBER'
                         )
else:
    print(f"No significant change in {STOCK} price")


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
