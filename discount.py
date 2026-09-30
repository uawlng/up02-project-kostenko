"""Модуль расчёта скидки."""
import sqlite3
from config import DB_PATH


def get_product_quantity(product_id):
    """
    Возвращает количество товара на складе.

    :param product_id: id товара
    :return: количество (int)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def calculate_price_with_discount(product_id, price):
    """
    Рассчитывает цену со скидкой 30%, если товара меньше 3.

    :param product_id: id товара
    :param price: базовая цена
    :return: цена со скидкой или без
    """
    quantity = get_product_quantity(product_id)

    if quantity < 3:
        return price * 0.70    # скидка 30%
    return price