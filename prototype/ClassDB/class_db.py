import sqlite3


class Database:

    def __init__(self, name):
        self.name = name

    def ADD(self, id_phot, name_pizza, description_pizza, price_pizza):
        db = sqlite3.connect(self.name)
        cursor = db.cursor()
        cursor.execute("INSERT INTO menu(id_photo, name_pizza, description_pizza, price_pizza) VALUES (?, ?, ?, ?)",
                       (id_phot, name_pizza, description_pizza, price_pizza))
        db.commit()
        db.close()

    def DELETE(self, name_pizza, price_pizza):
        db = sqlite3.connect(self.name)
        cursor = db.cursor()
        cursor.execute("DELETE FROM menu WHERE name_pizza = ? AND price_pizza = ?", (name_pizza, price_pizza))
        db.commit()
        db.close()

    def MENU_DISPLAY(self):
        db = sqlite3.connect(self.name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM menu")
        menu = cursor.fetchall()
        db.commit()
        db.close()
        return menu


if __name__ == '__main__':
    print('This is file class database.')
