import sqlite3
import pandas as pd

class Users:

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
        CREATE TABLE IF NOT EXISTS users
              (user_id text, username text, chat_id text, status text);
        """
        self._stmt_executer(stmt)

    def adduser(self, user_id, username, chat_id, status):
        stmt = f"""INSERT INTO users ('user_id','username','chat_id','status')
                VALUES ('{user_id}','{username}','{chat_id}','{status}')"""
        self._stmt_executer(stmt)

    def update_user_status(self, user_id, status):
        stmt = f"UPDATE users SET status = '{status}' WHERE user_id = '{user_id}' "
        self._stmt_executer(stmt)

    def get_users_to_update(self):
        stmt = f"SELECT user_id FROM users WHERE status = 'YES' "
        self._stmt_executer(stmt)
        return self._stmt_executer(stmt, get_data=True)

    def get_users_id(self):
        stmt = f"SELECT user_id FROM users"
        self._stmt_executer(stmt)
        return self._stmt_executer(stmt, get_data=True)

    def get_user_status(self, user_id):
        stmt = f"SELECT status  FROM users WHERE user_id = '{user_id}' "
        self._stmt_executer(stmt)
        return self._stmt_executer(stmt, get_data=True)

    def get_users_chatid_to_update(self):
        stmt = f"SELECT chat_id FROM users WHERE status = 'YES' "
        self._stmt_executer(stmt)
        return self._stmt_executer(stmt, get_data=True)