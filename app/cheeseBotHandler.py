from flask import Flask
from flask import request
from flask import Response
from flask_sslify import SSLify
from cheeseprice import getCheesePrice
from mortgage import Mortgage
from botutils import parse_message, send_message
from tokens import gipo_token, cheeze_token
from datetime import datetime
from prices import Prices
# from users import Users


def cheesebothandler():
    """
    Обрабатывает запросы к сырному боту
    :return:
    """
    if request.method == 'POST':
        msg = request.get_json()
        parsed = parse_message(msg)

        if parsed['txt'] == '/price':

            cheeze_price = getCheesePrice()
            current_date = datetime.today().strftime("%d-%m-%Y")
            send_message(parsed['chat_id'], cheeze_token, f"На {current_date}")

            all_dates = list(set([x[0] for x in p.show_dates()]))

            if current_date in all_dates:
                list_of_prices = p.show_prices_by_date(current_date)
                for el in list_of_prices:
                    send_message(parsed['chat_id'], cheeze_token, f"{el[1]}:{el[2]} ")
            else:

                for k, v in cheeze_price.items():
                    p.addprice('00000', k, v, current_date)
                list_of_prices = p.show_prices_by_date(current_date)

                for el in list_of_prices:
                    send_message(parsed['chat_id'], cheeze_token, f"{el[1]}:{el[2]} ")

            return Response('Ok', status=200)

        else:
            send_message(parsed['chat_id'], cheeze_token, parsed['txt'])
            return Response('Ok', status=200)
    else:
        return '<h1>Cheeeese</h1>'