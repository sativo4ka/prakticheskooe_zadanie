import sqlite3
import os

class DeliveryDB:
    def __init__(self, db_path="data/delivery.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER REFERENCES customers(id) ON DELETE RESTRICT,
                order_date TEXT NOT NULL,
                status TEXT CHECK(status IN ('новый','в доставке','выполнен','отменён')),
                total REAL NOT NULL
            )
        """)
        self.conn.commit()

    def add_customer(self, name, phone, address):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
        self.conn.commit()

    def get_customers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()

    def delete_customer(self, customer_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Ошибка: Нельзя удалить клиента, у которого есть заказы!")

    def add_order(self, customer_id, order_date, status, total):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO orders (customer_id, order_date, status, total) VALUES (?, ?, ?, ?)",
                       (customer_id, order_date, status, total))
        self.conn.commit()

    def get_orders(self, status=None):
        cursor = self.conn.cursor()
        if status:
            cursor.execute("SELECT * FROM orders WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM orders")
        return cursor.fetchall()

    def get_revenue_by_period(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(total) FROM orders WHERE status = 'выполнен'")
        return cursor.fetchone()[0] or 0.0

if __name__ == "__main__":
        db = DeliveryDB()

        if not db.get_customers():
            db.add_customer("Александра Карпухина", "+79991112233", "Москва, ул. Ленина, д. 10, кв. 5")
            db.add_customer("Парин Максим", "+79164445566", "Санкт-Петербург, Невский пр., д. 25")
            db.add_customer("Дмитрий Морозов", "+79037778899", "Новосибирск, ул. Кирова, д. 42")
            db.add_customer("Евгения Диколенко", "+79852223344", "Екатеринбург, ул. Малышева, д. 15, кв. 89")
            db.add_customer("Ибраев Асмир", "+79995556677", "Казань, ул. Баумана, д. 7")

            print("Создано 5 разных клиентов!")

            db.add_order(customer_id=1, order_date="2026-06-15", status="выполнен", total=1200.0)
            db.add_order(customer_id=1, order_date="2026-06-18", status="новый", total=850.0)

            db.add_order(customer_id=2, order_date="2026-06-17", status="в доставке", total=3100.0)

            db.add_order(customer_id=3, order_date="2026-06-18", status="выполнен", total=2500.0)

            db.add_order(customer_id=4, order_date="2026-06-16", status="выполнен", total=4500.0)

            db.add_order(customer_id=5, order_date="2026-06-18", status="отменён", total=150.0)

            print("Тестовые заказы для 5 клиентов успешно добавлены!")