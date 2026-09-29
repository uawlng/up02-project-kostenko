"""Загрузка заказов из БД."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_all_orders():
    """Возвращает список объектов Order из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # JOIN: берём заказ и товар, к которому он относится
    cur.execute("""
        SELECT Заказ.id, Заказ.дата, Заказ.клиент,
               Заказ.количество,
               Товар.id, Товар.категория, Товар.наименование,
               Товар.материал, Товар.цена, Товар.количество, Товар.фото
        FROM Заказ
        JOIN Товар ON Заказ.товар_id = Товар.id
        ORDER BY Заказ.id
    """)
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        # Сначала собираем объект Product из полей товара
        product = Product(
            product_id=row[4],
            category=row[5],
            name=row[6],
            material=row[7],
            price=row[8],
            quantity=row[9],
            image=row[10]
        )

        # Потом создаём объект Order
        order = Order(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product,
            quantity=row[3]
        )
        orders.append(order)

    return orders


def print_orders(orders):
    """Выводит информацию о заказах."""
    print(f"\nВсего заказов: {len(orders)}\n")
    for o in orders:
        print(o.info())
        print("-" * 70)

    # Итоговая сумма
    total_sum = sum(o.total() for o in orders)
    print(f"\nИТОГО по всем заказам: {total_sum} руб.")


if __name__ == "__main__":
    orders = get_all_orders()
    print_orders(orders)