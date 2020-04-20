import base64
import io

import pandas as pd
import matplotlib.pyplot as plt
from cachetools import cached, TTLCache

from statsmodels.tsa.arima_model import ARIMA

from flask import Flask, request, render_template, jsonify, abort

app = Flask(__name__)
categories = ['confirmed_US', 'deaths_US', 'deaths_global', 'recovered_global']


@app.route('/liveness')
def alive():
    return "OK"


@app.route('/')
def root():
    return render_template("index.html", categories=categories, category=categories[0], key='Massachusetts, US',
                           num_of_days=3, p=0, q=1, d=1)


@app.route('/forecast', methods=['POST'])
def response():
    category = request.form.get("category")
    key = request.form.get("key")
    num_of_days = int(request.form.get("num_of_days", "3"))
    p = int(request.form.get("p", "0"))
    q = int(request.form.get("q", "1"))
    d = int(request.form.get("d", "1"))

    plot_data = forecast(category, key, num_of_days, d, p, q)
    if not plot_data:
        abort(404)

    return render_template("index.html", categories=categories, category=category, key=key,
                           num_of_days=num_of_days, p=p, q=q, d=d, plot=plot_data)


@app.route('/forecast')
def get_forecast():
    category = request.args.get("category", categories[0])
    key = request.args.get("key", 'Massachusetts, US' if category.endswith('_US') else 'Turkey')
    num_of_days = int(request.args.get("num_of_days", "3"))
    p = int(request.args.get("p", "0"))
    q = int(request.args.get("q", "1"))
    d = int(request.args.get("d", "1"))

    plot_data = forecast(category, key, num_of_days, d, p, q)
    if not plot_data:
        abort(404)

    return jsonify({'plot': plot_data})


def forecast(category: str, key: str, num_of_days: int, d: int, p: int, q: int):
    df = read_csv(category)

    app.logger.info('Aggregating by ' + key)
    krs = [k for k in df.index if key in k]
    if len(krs) < 1:
        return None
    dr = df.loc[krs, df.columns[11:]].sum()

    app.logger.info('Forecasting {} day(s) out using ARIMA with order=({},{},{})'.format(num_of_days, p, q, d))
    model = ARIMA(dr.values, order=(p, q, d))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(len(dr.values), len(dr.values) + num_of_days, typ='levels')

    app.logger.info('Preparing plot...')
    plt.figure(figsize=(10, 10), dpi=100)
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(dr.index[-num_of_days:], dr.values[-num_of_days:], color='tab:red')
    ax1.set(title='COVID-19 ' + category + ' ' + key, xlabel='dates', ylabel='num of ' + category)
    ax2.plot(range(0, len(yhat)), yhat, color='tab:blue')
    ax2.set(xlabel='days', ylabel=category + ' forecast')

    app.logger.info('Converting plot to png...')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)

    plot_data = base64.b64encode(img.getvalue()).decode()

    return plot_data


@cached(cache=TTLCache(maxsize=1024, ttl=3*60*60))
def read_csv(cat: str) -> pd.DataFrame:
    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master'
    url = base_url + '/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + cat + '.csv'
    idx = 'Combined_Key' if cat.endswith('_US') else 'Country/Region'
    app.logger.info('Reading CSV from ' + url + " and indexing on " + idx)
    return pd.read_csv(url, index_col=idx)


if __name__ == '__main__':
    app.run(host="0.0.0.0")