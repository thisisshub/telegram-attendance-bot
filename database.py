import sqlite3

class DBHelper:
    def __init__(self, dbname="attendance.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS SUBJECTS (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO SUBJECTS (description) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM SUBJECTS"
        return [x[0] for x in self.conn.execute(stmt)]
