from flask import Flask
from flask import request
from flask import Response
from flask_sslify import SSLify
from cheeseprice import getCheesePrice
from mortgage import Mortgage
from botutils import parse_message, send_message
from tokens import gipo_token, cheeze_token
from datetime import datetime, timedelta
from prices import Prices
from calculatorBotHandler import inner_gipo_handler

prices_db = "prices.sqlite3"
users_db = "users.sqlite3"

p = Prices(prices_db)
p.create_tab()
u = Users(users_db)

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>Buongiorno!!!</h1>'


@app.route('/gipo', methods=['POST', 'GET'])
def outer_gipo_handler():
    inner_gipo_handler()


@app.route('/cheeze', methods=['POST', 'GET'])
def cheesebothandler():
    """
    Обрабатывает запросы к сырному боту
    :return:
    """
    if request.method == 'POST':
        msg = request.get_json()
        parsed = parse_message(msg)

        if parsed['txt'] == '/price':

            # cheeze_price = getCheesePrice()
            current_date = datetime.today().strftime("%d-%m-%Y")
            yesterday_date = datetime.today() - timedelta(days=1)
            yesterday_date = yesterday_date.strftime("%d-%m-%Y")
            send_message(parsed['chat_id'], cheeze_token, f"На {current_date} цены на сыр таковы:")

            all_dates = list(set([x[0] for x in p.show_dates()]))

            if current_date in all_dates:
                list_of_prices = p.show_prices_by_date(current_date)
                for el in list_of_prices:
                    send_message(parsed['chat_id'], cheeze_token, f"{el[1]}:{el[2]} ")
                # p.compare_prices(yesterday_date, current_date)
            else:
                cheeze_price = getCheesePrice(save_to_db=True)
                list_of_prices = p.show_prices_by_date(current_date)
                for el in list_of_prices:
                    send_message(parsed['chat_id'], cheeze_token, f"{el[1]}:{el[2]} ")

            return Response('Ok', status=200)

        else:
            send_message(parsed['chat_id'], cheeze_token, parsed['txt'])
            return Response('Ok', status=200)
    else:
        return '<h1>Cheeeese</h1>'





if __name__ == '__main__':
    app.run()
