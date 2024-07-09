import sqlite3
from typing import Union


class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table_payments(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            payments_id TEXT,
            first_name TEXT,
            coin_type TEXT,
            coin_amount TEXT,
            username TEXT NULL,
            credit_card TEXT,
            credit_card_placeholder TEXT,
            credit_card_exp_date TEXT,
            status BOOL NULL,
            payed BOOL NULL,
            created_at TEXT
        );
        
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def create_table_narx(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Narxlar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UZS TEXT,
            DOLLAR TEXT,
            NOTCOIN TEXT,
            HAMSTER TEXT,
            TAPSWAP TEXT,
            updated_at
        
        );
        
        
        """
        self.cursor.execute(sql)
        self.conn.commit()


    def create_table_coins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Coins(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            sell_now BOOL,
            updated_at TEXT
            
        
        
        );
        
        
        """

        self.cursor.execute(sql)
        self.conn.commit()

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NULL,
            last_name TEXT NULL,
            username TEXT,
            telegram_id INTEGER,
            added_at TEXT,
            credit_card TEXT,
            credit_card_placeholder TEXT,
            credit_card_exp_date TEXT
            
        );
        """
        self.cursor.execute(sql)
        self.conn.commit()


    def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NULL,
            last_name TEXT NULL,
            username TEXT,
            telegram_id INTEGER NOT NULL UNIQUE,
            added_at TEXT NULL
            
        );
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def new_narxlar(self, UZS: str, DOLLAR: str, NOTCOIN: str, HAMSTER: str, TAPSWAP: str, updated_at: str):
        sql = "INSERT INTO Narxlar(UZS, DOLLAR, NOTCOIN, HAMSTER, TAPSWAP, updated_at) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (UZS, DOLLAR, HAMSTER, NOTCOIN, TAPSWAP, updated_at))
        self.conn.commit()

    def add_coin(self, name: str, price: str, sell_now: bool, updated_at: str):
        sql = "INSERT INTO Coins(name, price, sell_now, updated_at) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (name, price, sell_now, updated_at))
        self.conn.commit()

    def add_payment(self, user_id: int, payments_id: int, first_name: str, coin_type: str, coin_amount: int, username: str, credit_card: str, credit_card_placeholder: str, credit_card_exp_date: str, status: bool, payed: bool, created_at: str):
        sql = "INSERT INTO Payments(user_id, payments_id, first_name, coin_type, coin_amount, username, credit_card, credit_card_placeholder, credit_card_exp_date, status, payed, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (user_id, payments_id, first_name, coin_type, coin_amount, username, credit_card, credit_card_placeholder, credit_card_exp_date, status, payed, created_at))
        self.conn.commit()

    def add_admin(self, first_name, last_name, username, telegram_id, added_at):
        sql = "INSERT INTO Admins (first_name, last_name, username, telegram_id, added_at) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (first_name, last_name, username, telegram_id, added_at))
        self.conn.commit()



    def add_user(self, first_name: str, last_name: str,  username: Union[str, None], telegram_id: int, credit_card: None, credit_card_placeholder: None, credit_card_exp_date: None, added_at: Union[str, None] = None):
        sql = "INSERT INTO Users (first_name, last_name, username, telegram_id, credit_card, credit_card_placeholder, credit_card_exp_date, added_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (first_name, last_name, username, telegram_id, credit_card, credit_card_placeholder, credit_card_exp_date, added_at))
        self.conn.commit()

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_all_payments(self):
        sql = "SELECT * FROM Payments"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_all_coins(self):
        sql = "SELECT * FROM Coins"
        self.cursor.execute(sql)
        coins = self.cursor.fetchall()
        return coins




    def get_user_telegram_id(self, telegram_id: int):
        sql = "SELECT * FROM users WHERE telegram_id = ?"
    
        # SQL so'rovni bajarish
        self.cursor.execute(sql, (telegram_id,))
        
        # Natijani olish
        user = self.cursor.fetchone()
        
        return user

    def check_user_exists(self, telegram_id):
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = ?)"
        self.cursor.execute(query, (telegram_id,))

        result = self.cursor.fetchone()[0]

        return bool(result)

    def check_payments_id_exists(self, payments_id):
        sql = "SELECT EXISTS(SELECT 1 FROM Payments WHERE payments_id = ?)"
        self.cursor.execute(sql, (payments_id,))
        result = self.cursor.fetchone()[0]

        return bool(result)

    def check_credit_card_exists(self, telegram_id):
        sql = "SELECT EXISTS(SELECT 1 FROM Users IS NULL WHERE telegram_id = ?)"
        self.cursor.execute(sql, (telegram_id,))
        result = self.cursor.fetchone()[0]

        return bool(result)

    def get_all_prices(self):
        sql = "SELECT * FROM Narxlar"
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_old_narxlar(self):
        sql = "DELETE * FROM Narxlar"
        self.cursor.execute(sql)
        self.conn.commit()


    def get_all_zakaslar(self):
        sql = "SELECT * FROM Payments"
        self.cursor.execute(sql)
        all_zakaslar =  self.cursor.fetchall()

        return all_zakaslar


    def get_history_payments_telegram_id(self, user_id):
        sql = "SELECT * FROM Payments WHERE user_id = ?"

        self.cursor.execute(sql, (user_id, ))

        history = self.cursor.fetchall()

        return history

    def get_zakas_payments_id(self, payments_id):
        sql = "SELECT * FROM Payments WHERE payments_id = ?"
        self.cursor.execute(sql, (payments_id, ))

        zakas = self.cursor.fetchone()

        return zakas

    def get_valyuta_name(self, name):
        sql = "SELECT * FROM Coins WHERE name = ? "
        self.cursor.execute(sql, (name, ))

        valyuta = self.cursor.fetchone()

        return valyuta


    def get_payments_status_none(self):
        sql = "SELECT * FROM Payments WHERE status IS NULL"
        self.cursor.execute(sql)
        payments = self.cursor.fetchall()
        return payments



    def get_payments_payed_none(self):
        sql = "SELECT * FROM Payments WHERE payed IS NULL"
        self.cursor.execute(sql)
        payments = self.cursor.fetchall()
        return payments

    def is_student_full_name(self, telegram_id: int) -> bool:
        user = self.get_user_telegram_id(telegram_id=telegram_id)

        if user and user[8] is not None:
            return True
        else:
            return False


    def is_card_number(self, telegram_id: int) -> bool:
        user = self.get_user_telegram_id(telegram_id=telegram_id)
        if user and user[6] is not None:
            return True
        else:
            return False

    def update_user_full_name(self, chat_id, full_name):
        data = (full_name, chat_id)
        sql = "UPDATE Users SET full_name = ? WHERE telegram_id = ?"
        self.cursor.execute(sql, data)
        self.conn.commit()

    def update_credit_card(self, chat_id, credit_card, credit_card_placeholder):
        data = (credit_card, credit_card_placeholder, chat_id)
        sql = "UPDATE Users SET credit_card = ?, credit_card_placeholder = ? WHERE telegram_id = ?"
        self.cursor.execute(sql, data)
        self.conn.commit()

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        conditions = [f"{key} = ?" for key in kwargs.keys()]
        sql += " AND ".join(conditions)
        values = tuple(kwargs.values())
        self.cursor.execute(sql, values)
        return self.cursor.fetchone()

    def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]



    def update_payments_status(self, status: bool, payments_id):
        sql = "UPDATE Payments SET status = ? WHERE payments_id = ?"
        self.cursor.execute(sql, (status, payments_id))
        self.conn.commit()

    def update_payments_payed(self, payed: bool, payments_id):
        sql = "UPDATE Payments SET payed = ? WHERE payments_id = ?"
        self.cursor.execute(sql, (payed, payments_id))
        self.conn.commit()

    def update_user_username(self, username: str, telegram_id: int):
        sql = "UPDATE Users SET username = ? WHERE telegram_id = ?"
        self.cursor.execute(sql, (username, telegram_id))
        self.conn.commit()

    def update_coin_narx(self, name: str, narx, updated_at):
        sql = "UPDATE Coins SET narx = ?, updated_at = ? WHERE name = ?"
        self.cursor.execute(sql, (name, narx, updated_at))
        self.conn.commit()


    def delete_users(self):
        sql = "DELETE FROM Users"
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_user(self, telegram_id):
        try:


            # Payments jadvalidan foydalanuvchiga tegishli barcha ma'lumotlarni o'chirish
            payments_sql = "DELETE FROM Payments WHERE user_id = ?"
            self.cursor.execute(payments_sql, (telegram_id,))

            # Users jadvalidan foydalanuvchini o'chirish
            users_sql = "DELETE FROM Users WHERE telegram_id = ?"
            self.cursor.execute(users_sql, (telegram_id,))

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Xatolik yuz berdi: {e}")
            return False
       


    def delete_coin(self, name):
        try:
            sql = "DELETE FROM Coins WHERE name = ?"
            self.cursor.execute(sql, (name, ))
            self.conn.commit()
            return True

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Xatolik: {e} ")
            return False




    def drop_users(self):
        sql = "DROP TABLE Users"
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()