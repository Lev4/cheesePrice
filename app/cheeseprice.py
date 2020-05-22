from bs4 import BeautifulSoup
import requests
from datetime import datetime
from prices import Prices
prices_db = "prices.sqlite3"



def getCheesePrice(save_to_db=False):

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
            for k, v in cheeze_price.items():
                p.addprice(cheesePriceId[k], k, v, current_date)
            print("add to db")
        else:
            print(f"На {current_date} уже загружены цены")


    return cheesePrice


if __name__ == '__main__':
    getCheesePrice(save_to_db=True)
