from flask import Flask, render_template, request
import pandas as pd
from datetime import date, timedelta
# import json
app = Flask(__name__)

data = pd.read_excel('C:/Users/rohit/Downloads/Book2.xlsx')


def get_today_date():
    today = date.today()
    return today.strftime("%m/%d/%Y")


def get_yesterday_date():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime("%m/%d/%Y")


def calculate_total_inbound_calls():
    return data['Inbound Call Volume'].sum()


def get_today_inbound_calls():
    today_date = get_today_date()
    today_calls = data[data['Date'] == today_date]['Inbound Call Volume'].sum()
    return today_calls


def get_yesterday_inbound_calls():
    yesterday_date = get_yesterday_date()
    yesterday_calls = data[data['Date'] == yesterday_date]['Inbound Call Volume'].sum()
    return yesterday_calls


def get_chart_dates():
    return data['Date'].tolist()


def get_inbound_calls_by_date(dataf):
    inbound_calls_by_date = {}
    for date_str in dataf['Date']:
        date_calls = data[data['Date'] == date_str]['Inbound Call Volume'].sum()
        date_str = date_str.strftime('%d/%m/%Y')
        inbound_calls_by_date[date_str] = int(date_calls)
    return inbound_calls_by_date


@app.route('/card', methods=['GET', 'POST'])
def index():
    total_calls = calculate_total_inbound_calls()
    today_calls = get_today_inbound_calls()
    yesterday_calls = get_yesterday_inbound_calls()

    inbound_calls_by_date = get_inbound_calls_by_date(data)

    if request.method == 'POST':
        data['Date'] = pd.to_datetime(data['Date'])

        start_date = pd.to_datetime(request.form['start_date'])
        end_date = pd.to_datetime(request.form['end_date'])

        # Filter the DataFrame based on the specified date range
        filtered_df = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
        inbound_calls_by_date = get_inbound_calls_by_date(filtered_df)

        total_inbound_calls = filtered_df['Inbound Call Volume'].sum()

        result = {
            "start_date": start_date.date().strftime('%Y-%m-%d'),
            "end_date": end_date.date().strftime('%Y-%m-%d'),
            "total_inbound_calls": total_inbound_calls,
            "details": inbound_calls_by_date
        }
    else:
        result = None

    return render_template('index.html', total_calls=total_calls,
                           today_calls=today_calls, yesterday_calls=yesterday_calls,
                           inbound_calls_by_date=inbound_calls_by_date, result=result)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8094)
