import requests
import pandas as pd
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = '<STOCK API>'
ALPHA_STOCK_URL = 'https://www.alphavantage.co/query'
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = '<NEWS API>'
TWILIO_SID = '<SID>'
TWILIO_AUTH_TOKEN = '<AUTH TOKEN>'
TWILIO_NUMBER = '<Twilio number'
RECEIVER_NUMBER = '<Number>'


def find_percentage():

    params = {
        'function': 'TIME_SERIES_WEEKLY_ADJUSTED',
        'symbol': STOCK_NAME,
        'apikey': STOCK_API
    }

    r = requests.get(ALPHA_STOCK_URL, params=params)
    data = r.json()['Weekly Adjusted Time Series']
    stock_dt = pd.DataFrame(data)

    close_values = stock_dt.iloc[3, 0:2].tolist()

    recent_week_close = float(close_values[0])
    past_week_close = float(close_values[1])
    absolute_difference = abs(recent_week_close - past_week_close)

    percentage = round((absolute_difference / recent_week_close * 100), 2)

    if past_week_close < recent_week_close:
        return f'{COMPANY_NAME} is up by {percentage}% from last week!'
    elif recent_week_close < past_week_close:
        return f'{COMPANY_NAME} is up down {percentage}% from last week!'
    else:
        return f'{COMPANY_NAME} has not changed since last week.'


def get_headlines():

    params = {
        'q': 'tesla',
        'sortBy': 'publishedAt',
        'apiKey': NEWS_API

    }

    r = requests.get(NEWS_ENDPOINT, params=params)
    data = r.json()

    headline1 = data['articles'][0]['title']
    url1 = data['articles'][0]['url']

    headline2 = data['articles'][1]['title']
    url2 = data['articles'][1]['url']

    headline3 = data['articles'][2]['title']
    url3 = data['articles'][2]['url']

    headlines = f"Here are today's top 3 headlines that could be affecting the market price for {COMPANY_NAME}:\n" \
                f"Headline 1: {headline1}\n" \
                f"Headline 2: {headline2}\n" \
                f"Headline 3: {headline3}"

    return headlines


def send_message():

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    message = client.messages \
                    .create(
                         body=f"\n{find_percentage()}\n{get_headlines()}",
                         from_=TWILIO_NUMBER,
                         to=RECEIVER_NUMBER)


send_message()

