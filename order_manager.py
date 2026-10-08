"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список кортежей (product_id, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Создаём заказ
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid

        # 2. Добавляем позиции И уменьшаем остатки
        for product_id, quantity, price in items:
            # Проверяем наличие
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")

            # Добавляем позицию
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, количество, цена) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )

            # Уменьшаем остаток
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )

        # 3. Фиксируем ВСЁ
        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()



def update_product_quantity(product_id, new_quantity):
    """
    Устанавливает новое количество товара в БД.
    :param product_id: id товара
    :param new_quantity: новое количество (перезаписывает текущее)
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Товар SET количество = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка обновления количества: {e}")


def decrease_product_quantity(product_id, quantity):
    """
    Уменьшает количество товара на складе.
    :param product_id: id товара
    :param quantity: на сколько уменьшить
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Проверяем, что товара достаточно
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return False

        current = row[0]
        if current < quantity:
            return False

        # Уменьшаем
        cur.execute(
            "UPDATE Товар SET количество = количество - ? WHERE id = ?",
            (quantity, product_id)
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления: {e}")
        return False

    finally:
        conn.close()


def get_product_quantity(product_id):
    """
    Возвращает текущее количество товара на складе.
    :param product_id: id товара
    :return: количество (int). Если товара нет — 0.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_items(order_id):
    """
    Возвращает состав заказа.
    :param order_id: id заказа
    :return: список кортежей (id, наименование, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Состав_заказа.id, Товар.наименование,
               Состав_заказа.количество,Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.
    :param order_id: id заказа
    :return: сумма (float)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(количество * цена)
        FROM Состав_заказа
        WHERE заказ_id = ?
    """, (order_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] or 0.0

def update_order_date(order_id, new_date):
    """
    Обновляет дату заказа.
    :param order_id: id заказа
    :param new_date: новая дата (YYYY-MM-DD)
    return: True при успехе, False при ошибке
    """
    conn= get_connection()
    cur=conn.cursor()

    try:
        cur.execute(
            "UPDATE Заказ SET дата = ? WHERE id = ?",
            (new_date, order_id)
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления даты: {e}")
        return False
    finally:
        conn.close()


def get_order_by_id(order_id):
    """
    Возвращает заказ по id.
    :param order_id: id заказа
    :return: кортеж (id, дата, клиент) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ WHERE id = ?",
                (order_id,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_order_item(item_id):
    """
    Удаляет позицию из состава заказа.
    :param item_id: id позиции
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Получаем данные позиции для восстановления остатков
        cur.execute("""
            SELECT товар_id, количество
            FROM Состав_заказа
            WHERE id = ?
        """, (item_id,))
        row = cur.fetchone()

        if not row:
            return False

        product_id, quantity = row

        #  Удаляем позицию
        cur.execute("DELETE FROM Состав_заказа WHERE id = ?", (item_id,))

        # Восстанавливаем остатки
        cur.execute("""
            UPDATE Товар
            SET количество = количество + ?
            WHERE id = ?
        """, (quantity, product_id))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка удаления позиции: {e}")
        return False

    finally:
        conn.close()




