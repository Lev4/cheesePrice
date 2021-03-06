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

        def _get_bot_data(self):

        self.home_value = int(input('Ввведите стоимость объекта: \n'))
        self.down_payment_percent = float(input('Ввведите первоначальный взнос в %: \n')) / 100
        self.mortgage_rate = float(input('Ввведите процентную ставку в %: \n')) / 100
        self.years = int(input('Ввведите количество лет ипотеки: \n'))

    def run(self):
        self._get_data()
        self.down_payment = self.home_value*self.down_payment_percent
        self.mortgage_loan = self.home_value - self.down_payment
        self.mortgage_rate_periodic = (1+self.mortgage_rate)**(1/12) - 1
        self.mortgage_payment_periods = self.years *12
        self.periodic_mortgage_payment = -1*np.pmt(self.mortgage_rate_periodic, self.mortgage_payment_periods, self.mortgage_loan)
        self.initial_interest_payment = self.mortgage_loan*self.mortgage_rate_periodic
        self.initial_principal_payment = self.periodic_mortgage_payment - self.initial_interest_payment

    def info(self):
        print(f'Первоначальный платеж: {self.down_payment}')
        print(f'Сумма кредита: {self.mortgage_loan}')
        print(f'Процентная ставка по кредиту : {self.mortgage_rate *100}%')
        print(f'Количетство лет кредита: {self.years}')
#         print(f'Периодическая процентная ставка :{self.mortgage_rate_periodic}')
        print(f'Количетсво периодов платежей: {self.mortgage_payment_periods}')
        print('_'*100)
        print(f"Ежемесячный платеж по кредиту: {round(self.periodic_mortgage_payment, 2)}" )
        print('_'*100)
        print(f"Первый платеж (проценты): {round(self.initial_interest_payment, 2)}")
        print(f"Первый платеж (основной долг): {round(self.initial_principal_payment, 2)}")
