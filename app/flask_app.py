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
from users import Users


prices_db = "prices.sqlite3"
users_db = "users.sqlite3"

p = Prices(prices_db)
p.create_tab()
u = Users(users_db)
u.create_tab()

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>Buongiorno!!!</h1>'


@app.route('/gipo', methods=['POST', 'GET'])
def gipo_handler():

   if request.method == 'POST':
       msg = request.get_json()
       parsed = parse_message(msg)

       if (not parsed['txt']):
           send_message(parsed['chat_id'], gipo_token, '...')
           return Response('Ok', status=200)

       elif parsed['txt'] == '/calc':
           send_message(parsed['chat_id'], gipo_token, 'Ввведите через разделитель следующие данные')
           send_message(parsed['chat_id'], gipo_token,
                        'стоимость объекта / первоначальный взнос в % / процентную ставку в % / количество лет ипотеки')
           send_message(parsed['chat_id'], gipo_token, 'Пример:')
           send_message(parsed['chat_id'], gipo_token, '3000000 / 20 / 10 / 30')
           return Response('Ok', status=200)

       elif len(parsed['txt'].split('/')) == 4:
           vals = parsed['txt'].split('/')
           m = Mortgage()
           m.home_value = int(vals[0])
           m.down_payment_percent = float(vals[1]) / 100
           vals[2] = vals[2].replace(',', '.')
           m.mortgage_rate = float(vals[2]) / 100
           m.years = int(vals[3])
           m.run()
           send_message(parsed['chat_id'], gipo_token, f'Cтоимость объекта: {m.home_value}')
           send_message(parsed['chat_id'], gipo_token, f'Первоначальный взнос в % : {m.down_payment_percent * 100}')
           send_message(parsed['chat_id'], gipo_token, f'Процентная ставка в %: {m.mortgage_rate * 100}')
           send_message(parsed['chat_id'], gipo_token, f'Первоначальный взнос: {m.down_payment}')
           send_message(parsed['chat_id'], gipo_token, f'Сумма кредита: {m.mortgage_loan}')
           send_message(parsed['chat_id'], gipo_token, f'Процентная ставка по кредиту : {m.mortgage_rate * 100}%')
           send_message(parsed['chat_id'], gipo_token, f'Количество лет кредита: {m.years}')
           send_message(parsed['chat_id'], gipo_token, f'Количетсво периодов платежей: {m.mortgage_payment_periods}')
           send_message(parsed['chat_id'], gipo_token,
                        f"Ежемесячный платеж по кредиту: {round(m.periodic_mortgage_payment, 2)}")
           send_message(parsed['chat_id'], gipo_token, f"Первый платеж (проценты): {round(m.initial_interest_payment, 2)}")
           send_message(parsed['chat_id'], gipo_token,
                        f"Первый платеж (основной долг): {round(m.initial_principal_payment, 2)}")
           return Response('Ok', status=200)

       else:
           send_message(parsed['chat_id'], gipo_token, '.....')
           return Response('Ok', status=200)




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
            usersss = u.get_users_id()
            print(usersss)
            if parsed['user_id'] not in usersss:
                u.adduser(parsed['user_id'], parsed['username'], "NO")
                print(f"add user {parsed['user_id']}")


            current_date = datetime.today().strftime("%d-%m-%Y")
            send_message(parsed['chat_id'], cheeze_token, f"На {current_date} цены на сыр таковы:")

            all_dates = list(set([x[0] for x in p.show_dates()]))

            if current_date in all_dates:
                list_of_prices = p.show_prices_by_date(current_date)
                for el in list_of_prices:
                    send_message(parsed['chat_id'], cheeze_token, f"{el[1]}:{el[2]} ")

            else:
                cheeze_price = getCheesePrice(save_to_db=True)
                list_of_prices = p.show_prices_by_date(current_date)
                for el in list_of_prices:
                    send_message(parsed['chat_id'], cheeze_token, f"{el[1]}:{el[2]} ")
            return Response('Ok', status=200)

        elif parsed['txt'] == '/subscription':
            users_to_update = u.get_users_to_update()
            if len(users_to_update) > 0:
                users_to_update = [x[0] for x in users_to_update]
            current_user_id = parsed['user_id']
            if current_user_id in users_to_update:
                subscribe_info_yes = """
                Вы подписаны на уведомления об изменениях цен.
                Для того чтобы отключить уведомления используйте команду /unsubscribe
                """
                send_message(parsed['chat_id'], cheeze_token, subscribe_info_yes)
                return Response('Ok', status=200)
            else:
                subscribe_info_no = """ 
                Вы не подписаны на уведомления об изменениях цен.
                Для того чтобы подписаться используйте команду /subscribe
                """
                send_message(parsed['chat_id'], cheeze_token, subscribe_info_no)
                return Response('Ok', status=200)

        elif parsed['txt'] == '/subscribe':
            current_user_id = parsed['user_id']
            subscribe_yes_message = """
            Вы подписаны на уведомления об изменениях цен.
            Для того чтобы отключить уведомления, используйте команду /unsubscribe
            """
            u.update_user_status(current_user_id, "YES")
            send_message(parsed['chat_id'], cheeze_token, subscribe_yes_message)
            return Response('Ok', status=200)

        elif parsed['txt'] == '/unsubscribe':
            current_user_id = parsed['user_id']
            subscribe_no_message = """
            Вы не подписаны на уведомления об изменениях цен.
            Если захотите получать уведомления, используйте команду /subscribe
            """
            u.update_user_status(current_user_id, "NO")
            send_message(parsed['chat_id'], cheeze_token, subscribe_no_message)
            return Response('Ok', status=200)

        else:
            send_message(parsed['chat_id'], cheeze_token, parsed['txt'])
            return Response('Ok', status=200)


    else:
        return '<h1>Cheeeese</h1>'


if __name__ == '__main__':
    app.run()
