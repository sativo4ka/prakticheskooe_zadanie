import pytest
import sqlite3
from database import DeliveryDB


@pytest.fixture
def test_db():
    db = DeliveryDB()
    db.conn = sqlite3.connect(":memory:")
    cursor = db.conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            city TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    """)
    db.conn.commit()
    yield db
    db.conn.close()


def test_add_and_get_customer(test_db):
    test_db.add_customer("Тестовый Клиент", "111222", "Москва")
    customers = test_db.get_customers()
    assert len(customers) == 1
    assert customers[0][1] == "Тестовый Клиент"
    assert customers[0][3] == "Москва"


def test_add_and_filter_orders(test_db):
    test_db.add_order(1, "2026-06-18", "новый", 500.0)
    test_db.add_order(1, "2026-06-18", "выполнен", 1200.0)

    all_orders = test_db.get_orders("Все")
    assert len(all_orders) == 2

    new_orders = test_db.get_orders("новый")
    assert len(new_orders) == 1
    assert new_orders[0][4] == 500.0


def test_revenue_calculation(test_db):
    test_db.add_order(1, "2026-06-18", "выполнен", 1000.0)
    test_db.add_order(1, "2026-06-18", "новый", 500.0)
    test_db.add_order(1, "2026-06-18", "выполнен", 250.50)

    revenue = test_db.get_revenue_by_period()
    assert revenue == 1250.50


def test_top_customers(test_db):
    test_db.add_customer("Лидер", "001", "Томск")
    test_db.add_customer("Второй", "002", "Омск")

    test_db.add_order(1, "2026-06-18", "выполнен", 100.0)
    test_db.add_order(1, "2026-06-18", "выполнен", 200.0)
    test_db.add_order(2, "2026-06-18", "выполнен", 500.0)

    top = test_db.get_top_customers()
    assert len(top) >= 2
    assert top