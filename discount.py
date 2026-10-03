"""Модуль расчёта скидки."""
import sqlite3
from config import DB_PATH


def get_product_quantity(product_id):
    """Возвращает количество товара на складе."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def calculate_price_with_discount(product_id, price):
    """Цена со скидкой 30%, если товара < 3. С защитой от None."""
    if price is None:
        return 0
    quantity = get_product_quantity(product_id)
    if quantity < 3:
        return price * 0.70
    return price