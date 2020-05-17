from bs4 import BeautifulSoup
import requests
from datetime import datetime

def getCheesePrice():

    cheesePriceId = {
        "Фестивальный" : "fest_24-price",
        "Истринский" : "ber_1-price",
        "Винный" : "vai_3-price",
        "Медовый" : "med_23-price",
        "Пивной" : "bir_5-price",
        "Тирольский" : "tirol_22-price",
        "Пошехонский" : "posh_76-price",
        "Колмогоровский" : "kolmo_15-price",
        "Золотой рубль" : "gold_16-price",
        "Губернаторский" : "gub_6-price",
        "Красногорский" : "krest_17-price",
        "Свежий для жарки" : "sve_7-price"
    }

    url = "https://parmezan.ru/Zakaz"
    res = requests.get(url)
    page = res.text
    soup = BeautifulSoup(page, 'html.parser')
    cheesePrice = {}

    for k, v in cheesePriceId.items():
        if soup.find(id=v) is not None:
            cheesePrice[k] = soup.find(id=v).text.strip()
            cheesePrice['date'] = datetime.today().strftime("%m-%d-%Y")

    return cheesePrice

if __name__ == '__main__':
    getCheesePrice()