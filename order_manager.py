"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_order(client, items):
    """Создаёт заказ с позициями. items = [(product_id, quantity, price), ...]"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (date, client))
        order_id = cur.lastrowid

        for product_id, quantity, price in items:
            cur.execute(
                "INSERT INTO Состав_заказа (заказ_id, товар_id, количество, цена) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )

        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None
    finally:
        conn.close()


def update_product_quantity(product_id, new_quantity):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Товар SET количество = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка обновления количества: {e}")


def get_product_quantity(product_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0
