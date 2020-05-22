import sqlite3


class Prices:

    def __init__(self, db):
        self.db = db

    def _stmt_executer(self, query, get_data=False):
        con = sqlite3.connect(self.db)
        c = con.cursor()
        if get_data:
            data_result = c.execute(query).fetchall()
            con.commit()
            con.close()

            return data_result
        else:
            c.execute(query)
            con.commit()
            con.close()

    def create_tab(self):

        stmt = """
        CREATE TABLE IF NOT EXISTS prices
              (cheese_id text, cheesename text, price text, date text);
        """
        self._stmt_executer(stmt)

    def addprice(self, cheese_id, cheesename, price, date):
        stmt = f"INSERT INTO prices ('cheese_id','cheesename','price', 'date') VALUES ('{cheese_id}','{cheesename}' ,'{price}','{date}')"
        self._stmt_executer(stmt)

    def update_price(self, cheese_id, price):
        stmt = f"UPDATE prices SET price = {price} WHERE cheese_id = {cheese_id} "
        self._stmt_executer(stmt)

    def show_prices(self):
        stmt = f"SELECT * FROM prices"
        return self._stmt_executer(stmt, get_data=True)

    def show_prices_by_date(self, target_date):
        stmt = f"SELECT * FROM prices WHERE date = '{target_date}'"
        return self._stmt_executer(stmt, get_data=True)

    def show_dates(self):
        stmt = f"SELECT date FROM prices "
        return self._stmt_executer(stmt, get_data=True)

    def compare_prices(self, date1, date2):
        """ Сравнивает цены на сыр по двум датам """

        cols = ['cheese_id', 'cheesename', 'price1', 'date']
        tab1 = pd.DataFrame(self.show_prices_by_date(date1), columns=cols).drop(['cheese_id', 'date'], axis=1)
        cols = ['cheese_id', 'cheesename', 'price2', 'date']
        tab2 = pd.DataFrame(self.show_prices_by_date(date2), columns=cols).drop(['cheese_id', 'date'], axis=1)
        tab = pd.merge(tab1, tab2, on="cheesename")
        tab['diff'] = tab['price1'].astype('int') - tab['price1'].astype('int')
        diff_dict = dict(zip(tab['cheesename'].tolist(), tab['diff'].tolist()))
        return diff_dict


