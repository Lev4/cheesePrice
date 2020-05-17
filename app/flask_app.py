
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask import Response
from flask_sslify import SSLify
from cheeseprice import getCheesePrice
from tokens import gipo_token, cheeze_token
import requests
import numpy as np


app = Flask(__name__)
sslify = SSLify(app)





def parse_message(message):
    parsed = dict()
    parsed['chat_id'] = message['message']['chat']['id']
    parsed['txt'] = message['message']['text']
    parsed['user_id'] = message['message']['from']['id']
    parsed['first_name'] = message['message']['from']['first_name']
    parsed['last_name'] = message['message']['from']['last_name']
    parsed['username'] = message['message']['from']['username']
    parsed['message_id'] = message['message']['message_id']
    parsed['update_id'] = message['update_id']
    parsed['mes_date'] = message['message']['date']
    return parsed

def send_message(chat_id, token, text='bla-bla-bla'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload)
    return r


class Mortgage():
    """
    Рассчитывает платежи по ипотеке
    """

    def __init__(self):
        self.home_value = None
        self.down_payment_percent = None
        self.down_payment = None
        self.mortgage_loan = None
        self.mortgage_rate = None
        self.years = None
        self.mortgage_rate_periodic=None
        self.mortgage_payment_periods = None
        self.periodic_mortgage_payment = None
        self.initial_interest_payment = None
        self.initial_principal_payment = None

    def _get_data(self):

        self.home_value = int(input('Ввведите стоимость объекта: \n'))
        self.down_payment_percent = float(input('Ввведите первоначальный взнос в %: \n')) / 100
        self.mortgage_rate = float(input('Ввведите процентную ставку в %: \n')) / 100
        self.years = int(input('Ввведите количество лет ипотеки: \n'))

    def run(self):
        self.down_payment = self.home_value*self.down_payment_percent
        self.mortgage_loan = self.home_value - self.down_payment
        self.mortgage_rate_periodic = (1+self.mortgage_rate)**(1/12) - 1
        self.mortgage_payment_periods = self.years *12
        self.periodic_mortgage_payment = -1*np.pmt(self.mortgage_rate_periodic, self.mortgage_payment_periods, self.mortgage_loan)
        self.initial_interest_payment = self.mortgage_loan*self.mortgage_rate_periodic
        self.initial_principal_payment = self.periodic_mortgage_payment - self.initial_interest_payment





@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>Buongiorno!!!</h1>'




@app.route('/gipo', methods=['POST', 'GET'])
def bothandler():
    """
    Обрабатывает запросы к боту
    :return:
    """
    if request.method == 'POST':
        msg = request.get_json()
        parsed = parse_message(msg)

        if (not parsed['txt']) :
            send_message(parsed['chat_id'], gipo_token, '...')
            return Response('Ok', status=200)

        elif parsed['txt'] == '/calc':
            send_message(parsed['chat_id'], gipo_token,'Ввведите через разделитель следующие данные')
            send_message(parsed['chat_id'], gipo_token, 'стоимость объекта / первоначальный взнос в % / процентную ставку в % / количество лет ипотеки')
            send_message(parsed['chat_id'], gipo_token, 'Пример:')
            send_message(parsed['chat_id'], gipo_token, '3000000 / 20 / 10 / 30')
            return Response('Ok', status=200)

        elif len(parsed['txt'].split('/')) == 4 :
            vals = parsed['txt'].split('/')
            m = Mortgage()
            m.home_value = int(vals[0])
            m.down_payment_percent = float(vals[1]) / 100
            vals[2] = vals[2].replace(',','.')
            m.mortgage_rate = float(vals[2]) / 100
            m.years = int(vals[3])
            m.run()
            send_message(parsed['chat_id'], gipo_token, f'Cтоимость объекта: {m.home_value}')
            send_message(parsed['chat_id'], gipo_token, f'Первоначальный взнос в % : {m.down_payment_percent * 100}')
            send_message(parsed['chat_id'], gipo_token, f'Процентная ставка в %: {m.mortgage_rate * 100}')
            send_message(parsed['chat_id'], gipo_token, f'Первоначальный взнос: {m.down_payment}')
            send_message(parsed['chat_id'], gipo_token, f'Сумма кредита: {m.mortgage_loan}')
            send_message(parsed['chat_id'], gipo_token, f'Процентная ставка по кредиту : {m.mortgage_rate *100}%')
            send_message(parsed['chat_id'], gipo_token, f'Количество лет кредита: {m.years}')
            send_message(parsed['chat_id'], gipo_token, f'Количетсво периодов платежей: {m.mortgage_payment_periods}')
            send_message(parsed['chat_id'], gipo_token, f"Ежемесячный платеж по кредиту: {round(m.periodic_mortgage_payment, 2)}")
            send_message(parsed['chat_id'], gipo_token, f"Первый платеж (проценты): {round(m.initial_interest_payment, 2)}")
            send_message(parsed['chat_id'], gipo_token, f"Первый платеж (основной долг): {round(m.initial_principal_payment, 2)}")


            return Response('Ok', status=200)

        else:
            send_message(parsed['chat_id'], gipo_token, '.....')
            return Response('Ok', status=200)
    else:
        return '<h1>Gipo</h1>'


@app.route('/cheeze', methods=['POST', 'GET'])
def cheesebothandler():
    """
    Обрабатывает запросы к боту
    :return:
    """
    if request.method == 'POST':
        msg = request.get_json()
        parsed = parse_message(msg)


        if parsed['txt'] == '/price':
            try:
                cheeze_price = getCheesePrice()
                send_message(parsed['chat_id'], cheeze_token, f"На {cheeze_price['date']}")
                for k, v in cheeze_price.items():
                    if k == "date":
                        pass
                    else:
                        send_message(parsed['chat_id'], cheeze_token, f"{k}:{v} руб/кг")
            except :
                print("Проблема с cheeze_price")
                cheeze_price = "-"
                send_message(parsed['chat_id'], cheeze_token, cheeze_price)

            return Response('Ok', status=200)

        else:
            send_message(parsed['chat_id'], cheeze_token, parsed['txt'])
            return Response('Ok', status=200)
    else:
        return '<h1>Cheeeese</h1>'



if __name__ == '__main__':
    app.run()
