from tkinter import *
import smtplib
import os
import requests
from email.message import EmailMessage

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
yesterday = "2026-08-12"
day_before = "2026-08-11"

date = "2026-08-01"

MY_EMAIL = os.environ["YOUR_EMAIL"]
MY_PASSWORD = os.environ["YOUR_PASS"]

latest_status = ""
latest_percentage = 0
latest_price = 0
latest_articles = []
latest_stock = ""

def search():
    global latest_status, latest_percentage, latest_price, latest_stock
    name_label.config(text=stock_entry.get())

    stock = stock_entry.get()
    latest_stock = stock

    # Change the stock info
    STOCK_Endpoint = 'https://www.alphavantage.co/query'
    stock_apikey = os.environ["STOCK_APIKEY"]
    stock_parameters = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': stock,
        'apikey': stock_apikey,
    }
    response = requests.get(STOCK_Endpoint, params=stock_parameters)
    response.raise_for_status()
    stock_data = response.json()

    # Calculations:
    closing_yesterday = float(stock_data['Time Series (Daily)'][yesterday]['4. close'])
    closing_day_before = float(stock_data['Time Series (Daily)'][day_before]['4. close'])

    difference = closing_yesterday - closing_day_before
    percentage = abs((difference / closing_day_before) * 100)

    price = float(stock_data['Time Series (Daily)'][yesterday]['4. close'])
    daily_change = percentage

    if percentage >= 0:
        if difference > 0:
            status = str('INCREASED ')
        elif difference < 0:
            status = str('DECLINED ')
        else:
            status = str('NO CHANGE')

    latest_status = status
    latest_percentage = percentage
    latest_price = price

    # Rewrite the stock labels
    current_price_label.config(text=f"Current Price: ${price:.2f}")
    daily_change_label.config(text=f"Daily Change: {daily_change:.2f}%")
    status_label.config(text=f"Status: {status}")

def get_news():
    global latest_articles
    name = company_name_entry.get()

    # Change news parameters
    news_endpoint = 'https://newsapi.org/v2/everything'
    news_apikey = os.environ["NEWS_APIKEY"]
    news_parameters = {
        'q': name,
        'searchIn': 'title',
        'from': date,
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': news_apikey,
    }

    news_response = requests.get(news_endpoint, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()


    latest_articles = articles = news_data['articles'][:2]
    article_pieces = []
    for article in articles:
        title = article.get('title')
        description = article.get('description')
        url = article.get('url')

        email_format = f"Headline: {title}\n\nAbout: {description}\n\n"
        article_pieces.append(email_format)
    article_format = "\n".join(article_pieces)

    actual_news_text.delete("1.0", END)
    actual_news_text.insert(END, article_format)

def send_alert():
    msg = EmailMessage()

    msg["Subject"] = "STOCK ALERT!!!"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL

    msg.set_content(
        f"{latest_stock}: {latest_status} {latest_percentage:.2f}%\n"
        f"Current Price: ${latest_price:.2f}\n\n"
        + "\n\n".join(
            f"Headline: {article.get('title')}\n"
            f"URL: {article.get('url')}"
            for article in latest_articles
        ))
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.send_message(msg)

def refresh():
    search()


window = Tk()
window.title("Stock Tracker")
window.config(padx=50, pady=20)

canvas = Canvas(width=500, height=700)
background_img = PhotoImage(file='stock_img.png')
canvas.create_image(240, 150, image=background_img)
canvas.create_line(0, 380, 500, 380, width=2)
canvas.create_text(240, 150, text="Stock Tracker", font=('Helvetica', 40, 'bold'))
canvas.grid(row=0,column=2)

name_label = Label(text="Company: ", font=('Helvetica', 14))
name_label.place(x=0, y=325)
stock_label = Label(window, text="Stock: ", font=('Helvetica', 14))
stock_label.place(x=0, y=285)
current_price_label = Label(window, text="Current Price:    $XXX.XX", font=('Helvetica', 14))
current_price_label.place(x=0, y=390)
daily_change_label = Label(window, text="Daily Change:    +/-X.XX%", font=('Helvetica', 14))
daily_change_label.place(x=0, y=420)
status_label = Label(window, text="Status:    INCREASED/DECREASED", font=('Helvetica', 14))
status_label.place(x=0, y=450)
latest_news_label = Label(window, text="Latest News:  ", font=('Helvetica', 14))
latest_news_label.place(x=0, y=530)

actual_news_text = Text(window, height=5, width=50, wrap=WORD)
actual_news_text.place(x=0, y=560)

news_scroller = Scrollbar(window, command=actual_news_text.yview)
news_scroller.place(x=450, y=560, height=100)


actual_news_text.config(yscrollcommand=news_scroller.set)

stock_entry = Entry(window, font=('Helvetica', 12))
stock_entry.place(x=70, y=287)
company_name_entry = Entry(window, font=('Helvetica', 12))
company_name_entry.place(x=0, y=350)

search_btn = Button(window, text='Search', font=('Helvetica', 12), command=search)
search_btn.place(x=280, y=280)
show_news = Button(window, text='Show News: ', font=('Helvetica', 12), width=20, command=get_news)
show_news.place(x=0, y=490)
send_btn = Button(window, text='✉ Send Alert', font=('Helvetica', 12), width=20, command=send_alert)
send_btn.place(x=0, y=650)
refresh_btn = Button(window, text='🔄 Refresh', font=('Helvetica', 12), width=20, command=search)
refresh_btn.place(x=220, y=650)



window.mainloop()