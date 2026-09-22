import requests
from email.message import EmailMessage
import smtplib
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
yesterday = "2026-08-11"
day_before = "2026-08-10"

MY_EMAIL = os.environ["YOUR_EMAIL"]
MY_PASSWORD = os.environ["YOUR_PASS"]

NEWS_Endpoint = 'https://newsapi.org/v2/everything'
news_apikey = os.environ["NEWS_APIKEY"]
news_parameters = {
    'q': COMPANY_NAME,
    'searchIn': 'title',
    'from': '2026-07-15',
    'language': 'en',
    'sortBy': 'publishedAt',
    'apiKey': news_apikey,
}

STOCK_Endpoint = 'https://www.alphavantage.co/query'
stock_apikey = os.environ["STOCK_APIKEY"]
stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': stock_apikey,
}

response = requests.get(STOCK_Endpoint, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()

closing_yesterday = float(stock_data['Time Series (Daily)'][yesterday]['4. close'])
closing_day_before = float(stock_data['Time Series (Daily)'][day_before]['4. close'])

difference = closing_yesterday - closing_day_before
percentage = abs((difference / closing_day_before) * 100)

news_response = requests.get(NEWS_Endpoint, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()


articles = news_data['articles'][:3]
article_pieces = []
for article in articles:
    title = article.get('title')
    description = article.get('description')
    url = article.get('url')

    email_format = f"Headline: {title}\nDescription: {description}\nURL: {url}"
    article_pieces.append(email_format)
artile_format = "\n".join(article_pieces)

# ⬆️ ⬇️
if percentage > 0:
    if difference > 0:
        status = 'INCREASED BY'
    else:
        status = 'DECLINED BY'
    msg = EmailMessage()
    msg["Subject"] = "STOCK ALERT!!!"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL

    msg.set_content(
        f"TSLA: {status} {percentage:.2f}%\n\n"
        + "\n\n".join(article_pieces)
    )
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.send_message(msg)