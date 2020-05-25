from bs4 import BeautifulSoup
from prices import Prices
from users import Users
from botutils import parse_message, send_message
from tokens import gipo_token, cheeze_token
from datetime import datetime, timedelta
import requests

prices_db = "prices.sqlite3"
users_db = "users.sqlite3"


def getCheesePrice(save_to_db=False, check_price=False):
    """ Залезает на сайт parmezan.ru и вытаскивает оттуда цены"""

    cheesePriceId = {
        "Фестивальный": "fest_24-price",
        "Истринский": "ber_1-price",
        "Винный": "vai_3-price",
        "Медовый": "med_23-price",
        "Пивной": "bir_5-price",
        "Тирольский": "tirol_22-price",
        "Пошехонский": "posh_76-price",
        "Колмогоровский": "kolmo_15-price",
        "Золотой рубль": "gold_16-price",
        "Губернаторский": "gub_6-price",
        "Красногорский": "krest_17-price",
        "Свежий для жарки": "sve_7-price"
    }

    url = "https://parmezan.ru/Zakaz"
    res = requests.get(url)
    page = res.text
    soup = BeautifulSoup(page, 'html.parser')
    cheesePrice = {}

    for k, v in cheesePriceId.items():
        if soup.find(id=v) is not None:
            cheesePrice[k] = soup.find(id=v).text.strip()

    if save_to_db:

        p = Prices(prices_db)
        p.create_tab()
        current_date = datetime.today().strftime("%d-%m-%Y")
        all_dates = list(set([x[0] for x in p.show_dates()]))

        if current_date not in all_dates:
            for k, v in cheesePrice.items():
                p.addprice(cheesePriceId[k], k, v, current_date)
            print("add to db")
        else:
            print(f"На {current_date} уже загружены цены")

    return cheesePrice


def send_updates():

    p = Prices(prices_db)
    p.create_tab()
    current_date = datetime.today().strftime("%d-%m-%Y")
    day_before_current_date = datetime.today() - timedelta(1)
    day_before_current_date = day_before_current_date.strftime("%d-%m-%Y")
    message = p.check_price_change(day_before_current_date, current_date)

    if len(message) > 0:

        u = Users(users_db)
        u.create_tab()
        where_to_send = u.get_users_chatid_to_update()

        if len(where_to_send) > 0:
            where_to_send = [x[0] for x in where_to_send]

            for user_chat_id in where_to_send:
                send_message(user_chat_id, cheeze_token, message)


if __name__ == '__main__':
    getCheesePrice(save_to_db=True, check_price=False)
    send_updates()