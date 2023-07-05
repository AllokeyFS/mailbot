import sqlite3


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None


    def connect(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()


    def create_user_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS telegramuser(
                            id INTEGER PRIMARY KEY,
                            first_name VARCHAR(40),
                            user_id INTEGER UNIQUE
                            )
                            ''')
        self.conn.commit()

    def insert_user(self, first_name, user_id):
        self.cursor.execute('''
                            INSERT INTO telegramuser(
                            first_name,
                            user_id) 
                            VALUES (?,?)
                            ''', (first_name, user_id))
        self.conn.commit()
    
    
    
    
    def check_user(self, user_id):
        self.cursor.execute('SELECT user_id FROM telegramuser WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result is not None:
            return True
        else:
            return False
    

    def mailing_message(self):
        self.cursor.execute('SELECT user_id FROM telegramuser ')
        result = self.cursor.fetchall()
        return result
    
    def name_select(self):
        self.cursor.execute('SELECT first_name FROM telegramuser ')
        result = self.cursor.fetchall()
        return result      


    def close(self):
        self.conn.close()